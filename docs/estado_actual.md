# Estado Actual del Proyecto — Punto de Retoma

**Última actualización:** Mayo 2026
**Fase activa:** Fase 1 — Fundamentos

---

## ✅ Completado hasta ahora

### Entorno local
- [x] Python 3.11.9 instalado — comando en Windows: `py` (no `python`)
- [x] pip 24.3.1
- [x] gcloud CLI 564.0.0
- [x] Git 2.41.0 configurado (user: Oriana Osorio / email: orianaosorio5@gmail.com)
- [x] Docker 25.0.3
- [x] VS Code

### GCP
- [x] Proyecto creado: `metro-medellin-analytics` (PROJECT_NUMBER: 904894047503)
- [x] Organización: `boa2132-org` (dominio personal — OK)
- [x] Facturación vinculada: `01C595-790E21-C7BD70`
- [x] Alerta de presupuesto: $80 USD con alertas al 50% / 90% / 100%
- [x] APIs habilitadas: BigQuery, Storage, Cloud Run, Cloud Functions, Cloud Scheduler, Pub/Sub, Artifact Registry, Cloud Build, Secret Manager, Vertex AI, Logging, Monitoring, IAM
- [x] Cuenta de servicio creada: `metro-pipeline-sa@metro-medellin-analytics.iam.gserviceaccount.com`
  - Roles: bigquery.dataEditor, bigquery.jobUser, storage.objectAdmin, secretmanager.secretAccessor
  - **Sin llave JSON** — se usa ADC (Application Default Credentials)
- [x] ADC configurado localmente: `gcloud auth application-default login`
- [x] Buckets Cloud Storage creados:
  - `gs://metro-medellin-raw`
  - `gs://metro-medellin-staging`
  - `gs://metro-medellin-archive`

### GitHub
- [x] Repositorio: https://github.com/OrianaOsorio/metro-medellin-gcp
- [x] Estructura de carpetas creada (ingestion/src, dbt/models/bronze-silver-gold, infra, notebooks, orchestration/flows-deployments, .github/workflows)
- [x] README.md completo
- [x] docs/setup_fase1.md creado
- [x] .gitignore actualizado (con protección de credenciales)

### BigQuery
- [x] Datasets creados: `bronze`, `silver`, `gold` en proyecto `metro-medellin-analytics`

### Python / Ingesta
- [x] Entorno virtual creado y activado: `.venv\Scripts\Activate.ps1`
- [x] `requirements.txt` creado e instalado (google-cloud-storage, google-cloud-bigquery, pandas, pyarrow, requests, python-dotenv)
- [x] Script de ingesta escrito: `ingestion/src/gtfs_loader.py`
  - Lee los 9 archivos GTFS (.txt)
  - Sube cada archivo a `gs://metro-medellin-raw/gtfs/YYYY-MM-DD/`
  - Carga a BigQuery `bronze.<tabla>` con WRITE_TRUNCATE
  - Agrega columnas de auditoría `_ingestion_date` y `_source_file`

---

## ⚠️ Pendiente inmediato — PRIMER COMANDO AL RETOMAR

El script fue escrito pero **aún no se corrió con éxito**. El intento anterior falló
porque el `--gtfs-dir` no llegó correctamente (path con tildes y espacios).

**Solución — usar path relativo (ejecutar desde la carpeta del repo):**

```powershell
# 1. Ir al repo
cd "D:\Nubes\GCP\Ingeniería de Datos e IA con GCP Edición 18 de Smart Data\Proyecto de transporte\metro-medellin-gcp"

# 2. Activar el entorno virtual
.venv\Scripts\Activate.ps1

# 3. Correr la ingesta con path relativo
python ingestion\src\gtfs_loader.py --gtfs-dir "..\..\GTFS-METRO-MEDELLIN"
```

Resultado esperado: 9 tablas cargadas en BigQuery bronze y 9 archivos en GCS.

---

## 🔜 Próximos pasos (después de la ingesta exitosa)

1. **Verificar en GCP Console** que llegaron los datos:
   - BigQuery → proyecto `metro-medellin-analytics` → dataset `bronze` → 9 tablas
   - Cloud Storage → bucket `metro-medellin-raw` → carpeta `gtfs/YYYY-MM-DD/`
2. **Empaquetar en Docker** — `ingestion/Dockerfile`
3. **Commit y push** de todo lo trabajado al repo GitHub
4. **Fase 2** — Transformaciones silver/gold con dbt

---

## Comandos de verificación rápida al retomar

```powershell
# Verificar proyecto GCP activo
gcloud config get project

# Verificar buckets
gcloud storage buckets list --project=metro-medellin-analytics

# Verificar datasets BigQuery
bq ls --project_id=metro-medellin-analytics

# Activar entorno virtual
.venv\Scripts\Activate.ps1
```

---

## Stack tecnológico del proyecto

| Capa | Herramienta |
|---|---|
| Ingesta | Python + Docker + Cloud Run Jobs |
| Orquestación | Prefect Cloud |
| Almacenamiento | Cloud Storage + BigQuery medallion (bronze/silver/gold) |
| Transformaciones SQL | dbt-core + BigQuery adapter |
| Modelos IA | BigQuery ML + Vertex AI |
| Asistente IA | Gemini API + RAG |
| Dashboards | Looker Studio |
| Infraestructura | Terraform |
| CI/CD | GitHub Actions |

## Datos de referencia rápida

- **Project ID GCP:** `metro-medellin-analytics`
- **Service Account:** `metro-pipeline-sa@metro-medellin-analytics.iam.gserviceaccount.com`
- **Región:** `us-central1`
- **Repo GitHub:** https://github.com/OrianaOsorio/metro-medellin-gcp
- **Datos GTFS locales:** `D:\Nubes\GCP\Ingeniería de Datos e IA con GCP Edición 18 de Smart Data\Proyecto de transporte\GTFS-METRO-MEDELLIN\`
- **Comando Python:** `python` (dentro del .venv) o `py` (fuera del .venv)
