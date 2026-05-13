-- BigQuery ML: modelo de demanda por estacion/hora
-- Predice num_departures dado: stop_id, route_id, hour_of_day, day_type
-- Algoritmo: Linear Regression (rapido de entrenar, interpretable, ideal para MVP)
CREATE OR REPLACE MODEL `metro-medellin-analytics.gold.model_demand`
OPTIONS (
  model_type          = 'LINEAR_REG',
  input_label_cols    = ['num_departures'],
  data_split_method   = 'AUTO_SPLIT',
  enable_global_explain = TRUE
) AS
SELECT
  stop_id,
  route_id,
  route_type_name,
  day_type,
  hour_of_day,
  num_departures
FROM `metro-medellin-analytics.gold.trips_per_stop_per_hour`;
