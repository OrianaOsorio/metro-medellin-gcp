-- Silver: rutas/lineas con nombre del tipo de transporte
CREATE OR REPLACE TABLE `metro-medellin-analytics.silver.dim_routes` AS
SELECT
  r.route_id,
  r.agency_id,
  TRIM(r.route_short_name)   AS route_short_name,
  TRIM(r.route_long_name)    AS route_long_name,
  r.route_type,
  CASE r.route_type
    WHEN 0 THEN 'Tranvia'
    WHEN 2 THEN 'Metro'
    WHEN 3 THEN 'Bus'
    WHEN 5 THEN 'Teleferico'
    ELSE 'Otro'
  END                        AS route_type_name,
  r.route_color,
  a.agency_name
FROM `metro-medellin-analytics.bronze.routes` r
LEFT JOIN `metro-medellin-analytics.bronze.agency` a
  ON r.agency_id = a.agency_id
WHERE r.route_id IS NOT NULL;
