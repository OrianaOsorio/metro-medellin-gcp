-- Evaluar el modelo entrenado (R2, MAE, MSE)
SELECT *
FROM ML.EVALUATE(MODEL `metro-medellin-analytics.gold.model_demand`);
