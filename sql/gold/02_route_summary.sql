-- Gold: resumen por ruta — frecuencia, estaciones cubiertas y tipo de servicio
CREATE OR REPLACE TABLE `metro-medellin-analytics.gold.route_summary` AS
SELECT
  r.route_id,
  r.route_short_name,
  r.route_long_name,
  r.route_type_name,
  r.agency_name,
  COUNT(DISTINCT t.trip_id)      AS total_trips,
  COUNT(DISTINCT fs.stop_id)     AS total_stops_served,
  COUNT(DISTINCT t.service_id)   AS num_service_types,
  -- Frecuencia promedio en hora punta (7-9am, Laboral)
  ROUND(
    COUNTIF(fs.departure_hour BETWEEN 7 AND 8 AND t.service_id = 'Laboral') /
    NULLIF(COUNT(DISTINCT CASE WHEN fs.departure_hour BETWEEN 7 AND 8 AND t.service_id = 'Laboral'
                               THEN fs.stop_id END), 0),
    1
  )                              AS avg_peak_departures_per_stop
FROM `metro-medellin-analytics.silver.dim_routes` r
LEFT JOIN `metro-medellin-analytics.silver.dim_trips` t
  ON r.route_id = t.route_id
LEFT JOIN `metro-medellin-analytics.silver.fact_schedule` fs
  ON t.trip_id = fs.trip_id
GROUP BY
  r.route_id, r.route_short_name, r.route_long_name,
  r.route_type_name, r.agency_name;
