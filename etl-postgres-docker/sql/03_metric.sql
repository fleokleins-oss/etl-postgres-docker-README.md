-- Simple metrics
SELECT
  COUNT(*)                AS total_rows,
  COUNT(DISTINCT user_id) AS distinct_users
FROM public.events;
