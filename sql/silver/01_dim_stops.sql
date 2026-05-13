-- Silver: estaciones limpias con coordenadas y nombre
CREATE OR REPLACE TABLE `metro-medellin-analytics.silver.dim_stops` AS
SELECT
  stop_id,
  TRIM(stop_name)                          AS stop_name,
  stop_lat,
  stop_lon,
  COALESCE(location_type, 0)               AS location_type,
  COALESCE(wheelchair_boarding, 0)         AS wheelchair_boarding
FROM `metro-medellin-analytics.bronze.stops`
WHERE stop_id IS NOT NULL
  AND stop_lat IS NOT NULL
  AND stop_lon IS NOT NULL;
