# Metro Medellín Analytics — Plataforma de Datos e IA en GCP

Plataforma analítica end-to-end sobre **Google Cloud Platform** construida con datos abiertos GTFS del Metro de Medellín, orientada a optimizar la movilidad urbana con impacto social.

---

## Descripción

Este proyecto implementa una arquitectura moderna de **Lakehouse** sobre GCP que integra, procesa y explota los datos abiertos del Metro de Medellín para generar:

- Predicciones de demanda por estación y franja horaria
- Recomendaciones de optimización de rutas y frecuencias
- Un asistente conversacional con IA generativa (Gemini)
- Detección de anomalías para mantenimiento predictivo

## Stack tecnológico

| Capa | Herramienta |
|---|---|
| Ingesta | Python + Docker + Cloud Run Jobs |
| Orquestación | Prefect Cloud |
| Almacenamiento | Cloud Storage + BigQuery (bronze/silver/gold) |
| Transformaciones | dbt-core + BigQuery adapter |
| Modelos de IA | BigQuery ML + Vertex AI |
| Asistente IA | Gemini API + RAG |
| Dashboards | Looker Studio |
| Infraestructura como código | Terraform |
| CI/CD | GitHub Actions |

## Estructura del repositorio

```
metro-medellin-gcp/
├── .github/workflows/     # Pipelines de CI/CD
├── dbt/                   # Transformaciones SQL con dbt
│   └── models/
│       ├── bronze/        # Datos crudos validados
│       ├── silver/        # Datos limpios y enriquecidos
│       └── gold/          # Modelo dimensional listo para consumo
├── docs/                  # Documentación técnica
├── infra/                 # Infraestructura como código (Terraform)
├── ingestion/             # Scripts Python de ingesta
│   └── src/
├── notebooks/             # Notebooks de exploración y experimentación
├── orchestration/         # Flujos de Prefect
│   ├── flows/
│   └── deployments/
└── README.md
```

## Plan de implementación

| Fase | Semanas | Estado | Entregables |
|---|---|---|---|
| 1 — Fundamentos | 1-2 | 🔄 En progreso | Setup GCP, ingesta GTFS, capa bronze |
| 2 — Modelado | 3-4 | ⏳ Pendiente | Capas silver/gold con dbt, dashboard descriptivo |
| 3 — Modelos de IA | 5-6 | ⏳ Pendiente | Predicción de demanda, anomalías, optimización |
| 4 — Asistente y entrega | 7-8 | ⏳ Pendiente | Asistente Gemini, documentación final, video demo |

## Fuente de datos

- **GTFS Metro de Medellín:** [datosabiertos-metrodemedellin.opendata.arcgis.com](https://datosabiertos-metrodemedellin.opendata.arcgis.com)
- **Especificación GTFS:** [gtfs.org/es](https://gtfs.org/es/)
- **Clima:** Open-Meteo API
- **Festivos Colombia:** Librería `holidays`

## Configuración del proyecto GCP

- **Project ID:** `metro-medellin-analytics`
- **Región principal:** `us-central1`
- **Presupuesto máximo:** USD $80 (con alertas al 50%, 90% y 100%)

## Autora

**Oriana Osorio**
Curso: Ingeniería de Datos e IA con GCP — Smart Data Edición 18

## Licencia

MIT License — ver [LICENSE](LICENSE)
