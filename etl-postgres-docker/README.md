# ETL → PostgreSQL (Docker)

A tiny, runnable ETL example:
- reads `data/sample.csv`
- cleans + de-dupes in Python
- loads into Postgres
- runs SQL steps (create table, dedupe, metric)

## Quick start

1) Copy env file:
```bash
cp .env.example .env
```

2) Start Postgres:
```bash
docker compose up -d
```

3) Create a venv + install deps:
```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

4) Run ETL:
```bash
python src/etl.py
```

## What gets created
- table: `public.events`
- metric query prints total rows and distinct users

## Files
- `sql/01_create_table.sql` creates schema/table
- `sql/02_dedupe.sql` removes duplicates
- `sql/03_metric.sql` simple metric query
