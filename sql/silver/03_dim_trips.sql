-- Silver: viajes con tipo de dia (Laboral / Sabado / Domingo-Festivo)
CREATE OR REPLACE TABLE `metro-medellin-analytics.silver.dim_trips` AS
SELECT
  t.trip_id,
  t.route_id,
  t.service_id,
  TRIM(t.trip_headsign)  AS trip_headsign,
  COALESCE(t.direction_id, 0) AS direction_id,
  COALESCE(c.monday, 0)    AS monday,
  COALESCE(c.tuesday, 0)   AS tuesday,
  COALESCE(c.wednesday, 0) AS wednesday,
  COALESCE(c.thursday, 0)  AS thursday,
  COALESCE(c.friday, 0)    AS friday,
  COALESCE(c.saturday, 0)  AS saturday,
  COALESCE(c.sunday, 0)    AS sunday
FROM `metro-medellin-analytics.bronze.trips` t
LEFT JOIN `metro-medellin-analytics.bronze.calendar` c
  ON t.service_id = c.service_id
WHERE t.trip_id IS NOT NULL;
