-- Create a simple events table
CREATE TABLE IF NOT EXISTS public.events (
  event_id   BIGINT NOT NULL,
  user_id    BIGINT NOT NULL,
  event_type TEXT   NOT NULL,
  event_ts   TIMESTAMPTZ NOT NULL
);

-- Optional index for analytics-like queries
CREATE INDEX IF NOT EXISTS idx_events_user_ts ON public.events (user_id, event_ts);
