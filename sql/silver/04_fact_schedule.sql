-- Silver: horarios detallados con hora de salida extraida del string HH:MM:SS
-- GTFS permite horas > 23 para viajes que cruzan medianoche (ej: 25:00 = 1am)
-- Se usa MOD(hora, 24) para normalizar al rango 0-23
CREATE OR REPLACE TABLE `metro-medellin-analytics.silver.fact_schedule` AS
SELECT
  st.trip_id,
  st.stop_id,
  st.stop_sequence,
  st.arrival_time,
  st.departure_time,
  CAST(SPLIT(st.departure_time, ':')[OFFSET(0)] AS INT64)           AS departure_hour_raw,
  MOD(CAST(SPLIT(st.departure_time, ':')[OFFSET(0)] AS INT64), 24)  AS departure_hour,
  CAST(SPLIT(st.departure_time, ':')[OFFSET(1)] AS INT64)           AS departure_minute,
  t.route_id,
  t.service_id,
  t.direction_id,
  t.trip_headsign
FROM `metro-medellin-analytics.bronze.stop_times` st
INNER JOIN `metro-medellin-analytics.silver.dim_trips` t
  ON st.trip_id = t.trip_id
WHERE st.departure_time IS NOT NULL
  AND st.departure_time != ''
  AND st.stop_id IS NOT NULL;
