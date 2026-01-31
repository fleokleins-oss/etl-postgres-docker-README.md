-- Remove exact duplicates (same event_id + user_id + event_type + event_ts)
WITH ranked AS (
  SELECT
    ctid,
    ROW_NUMBER() OVER (
      PARTITION BY event_id, user_id, event_type, event_ts
      ORDER BY ctid
    ) AS rn
  FROM public.events
)
DELETE FROM public.events e
USING ranked r
WHERE e.ctid = r.ctid
  AND r.rn > 1;
