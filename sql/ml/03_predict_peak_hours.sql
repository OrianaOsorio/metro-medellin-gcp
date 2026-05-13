-- Prediccion: cuantos viajes habra en cada estacion durante hora punta (7-9am) un dia Laboral
-- Util para dashboard y para decisiones operativas del Metro
SELECT
  predicted_num_departures,
  stop_id,
  route_id,
  day_type,
  hour_of_day
FROM ML.PREDICT(
  MODEL `metro-medellin-analytics.gold.model_demand`,
  (
    SELECT DISTINCT
      stop_id,
      route_id,
      route_type_name,
      'Laboral'  AS day_type,
      hour        AS hour_of_day
    FROM `metro-medellin-analytics.gold.trips_per_stop_per_hour`,
    UNNEST(GENERATE_ARRAY(7, 9)) AS hour
  )
)
ORDER BY predicted_num_departures DESC;
