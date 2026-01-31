import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample.csv"
SQL_DIR = ROOT / "sql"

def env(name: str, default: str | None = None) -> str:
    v = os.getenv(name, default)
    if v is None or v == "":
        raise RuntimeError(f"Missing env var: {name}")
    return v

def connect():
    host = env("POSTGRES_HOST", "localhost")
    port = int(env("POSTGRES_PORT", "5432"))
    db   = env("POSTGRES_DB", "etl_db")
    user = env("POSTGRES_USER", "etl_user")
    pw   = env("POSTGRES_PASSWORD", "etl_pass")

    conninfo = f"host={host} port={port} dbname={db} user={user} password={pw}"
    return psycopg.connect(conninfo)

def run_sql_file(cur, path: Path):
    sql = path.read_text(encoding="utf-8")
    cur.execute(sql)

def main():
    load_dotenv(ROOT / ".env")

    # 1) Read
    df = pd.read_csv(DATA_PATH)

    # 2) Clean & validate (simple example)
    required = ["event_id", "user_id", "event_type", "event_ts"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    df = df.dropna(subset=required)
    df["event_id"] = df["event_id"].astype("int64")
    df["user_id"] = df["user_id"].astype("int64")
    df["event_type"] = df["event_type"].astype("string")

    # Parse timestamp; keep timezone-aware if present
    df["event_ts"] = pd.to_datetime(df["event_ts"], utc=True, errors="coerce")
    df = df.dropna(subset=["event_ts"])

    # 3) Load
    with connect() as conn:
        with conn.cursor() as cur:
            # Create table
            run_sql_file(cur, SQL_DIR / "01_create_table.sql")

            # Insert rows
            rows = list(df.itertuples(index=False, name=None))
            cur.executemany(
                "INSERT INTO public.events (event_id, user_id, event_type, event_ts) VALUES (%s, %s, %s, %s)",
                rows,
            )

            # Dedupe in SQL
            run_sql_file(cur, SQL_DIR / "02_dedupe.sql")

            # Metric
            run_sql_file(cur, SQL_DIR / "03_metric.sql")
            total_rows, distinct_users = cur.fetchone()

        conn.commit()

    print("✅ Done")
    print(f"total_rows={total_rows}, distinct_users={distinct_users}")

if __name__ == "__main__":
    main()
