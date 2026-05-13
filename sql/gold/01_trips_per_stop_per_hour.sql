-- Gold: tabla analitica principal — viajes por estacion, hora y tipo de dia
-- Es la base para BigQuery ML (prediccion de demanda) y Looker Studio
CREATE OR REPLACE TABLE `metro-medellin-analytics.gold.trips_per_stop_per_hour` AS
SELECT
  fs.stop_id,
  s.stop_name,
  s.stop_lat,
  s.stop_lon,
  fs.route_id,
  r.route_short_name,
  r.route_type_name,
  fs.service_id                            AS day_type,
  fs.departure_hour                        AS hour_of_day,
  COUNT(*)                                 AS num_departures,
  COUNT(DISTINCT fs.trip_id)               AS num_distinct_trips
FROM `metro-medellin-analytics.silver.fact_schedule` fs
INNER JOIN `metro-medellin-analytics.silver.dim_stops` s
  ON fs.stop_id = s.stop_id
INNER JOIN `metro-medellin-analytics.silver.dim_routes` r
  ON fs.route_id = r.route_id
GROUP BY
  fs.stop_id, s.stop_name, s.stop_lat, s.stop_lon,
  fs.route_id, r.route_short_name, r.route_type_name,
  fs.service_id, fs.departure_hour;
