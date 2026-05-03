# Setup Fase 1 — Fundamentos del Proyecto

**Fecha:** Mayo 2026
**Responsable:** Oriana Osorio
**Objetivo:** Configurar el entorno local, el proyecto GCP y el repositorio de código.

---

## 1. Entorno local

### Herramientas instaladas

| Herramienta | Versión | Notas |
|---|---|---|
| Python | 3.11.9 | Instalado desde python.org. En Windows usar el comando `py` |
| pip | 24.3.1 | Incluido con Python |
| gcloud CLI | 564.0.0 | Google Cloud SDK |
| Git | 2.41.0 | |
| Docker | 25.0.3 | |
| VS Code | — | Editor principal |

### Notas de instalación Python en Windows

- Python debe instalarse desde **python.org** (NO desde Microsoft Store)
- Durante la instalación: marcar **"Add python.exe to PATH"**
- Hacer clic en **"Deshabilitar límite de longitud de ruta"** al finalizar
- El alias de la Microsoft Store (`WindowsApps/python.exe`) debe desactivarse en:
  `Configuración > Aplicaciones > Alias de ejecución de aplicaciones`
- En Windows, el comando correcto es `py` (lanzador oficial), no `python`

---

## 2. Proyecto Google Cloud Platform

### Datos del proyecto

| Parámetro | Valor |
|---|---|
| Project ID | `metro-medellin-analytics` |
| Project Number | `904894047503` |
| Organización | `boa2132-org` (dominio personal) |
| Región principal | `us-central1` |
| Billing Account ID | `01C595-790E21-C7BD70` |

### Créditos disponibles

- **Free Trial GCP:** ~$300 USD (1,099,063.19 COP)
- **Días restantes al inicio:** 65 días
- **Costo estimado del proyecto:** USD $49–60

### Alerta de presupuesto configurada

- **Nombre:** `alerta-metro-medellin`
- **Techo:** USD $80
- **Alertas:** 50% / 90% / 100%
- **Notificación:** email de la cuenta

### APIs habilitadas

```
bigquery.googleapis.com
storage.googleapis.com
run.googleapis.com
cloudfunctions.googleapis.com
cloudscheduler.googleapis.com
pubsub.googleapis.com
artifactregistry.googleapis.com
cloudbuild.googleapis.com
secretmanager.googleapis.com
aiplatform.googleapis.com
logging.googleapis.com
monitoring.googleapis.com
iam.googleapis.com
```

### Comando de habilitación usado

```bash
gcloud services enable bigquery.googleapis.com storage.googleapis.com run.googleapis.com cloudfunctions.googleapis.com cloudscheduler.googleapis.com pubsub.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com aiplatform.googleapis.com logging.googleapis.com monitoring.googleapis.com iam.googleapis.com --project=metro-medellin-analytics
```

---

## 3. Repositorio GitHub

| Parámetro | Valor |
|---|---|
| URL | https://github.com/OrianaOsorio/metro-medellin-gcp |
| Visibilidad | Público |
| Licencia | MIT |
| .gitignore | Python |

### Estructura de carpetas creada

```
metro-medellin-gcp/
├── .github/
│   └── workflows/
├── dbt/
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   └── tests/
├── docs/
│   └── setup_fase1.md     ← este archivo
├── infra/
├── ingestion/
│   └── src/
├── notebooks/
├── orchestration/
│   ├── deployments/
│   └── flows/
├── .gitignore
├── LICENSE
└── README.md
```

---

## 4. Comandos de referencia rápida

```powershell
# Verificar herramientas
py --version
gcloud --version
git --version
docker --version

# Configurar proyecto GCP activo
gcloud config set project metro-medellin-analytics
gcloud config get project

# Ver proyectos disponibles
gcloud projects list

# Ver APIs habilitadas
gcloud services list --enabled --project=metro-medellin-analytics
```

---

## 5. Próximos pasos (Fase 1 continúa)

- [ ] Crear cuenta de servicio con permisos mínimos (IAM)
- [ ] Crear buckets en Cloud Storage (raw / staging / archive)
- [ ] Crear datasets en BigQuery (bronze / silver / gold)
- [ ] Configurar entorno virtual Python con dependencias del proyecto
- [ ] Explorar y entender el archivo GTFS-METRO-MEDELLIN.zip
- [ ] Escribir script de ingesta GTFS en Python
- [ ] Empaquetar el script en Docker
- [ ] Subir primer commit con la estructura base
