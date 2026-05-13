"""
Carga archivos GTFS del Metro de Medellin a GCS (raw) y BigQuery (bronze).

Uso:
    python ingestion/src/gtfs_loader.py --gtfs-dir "..\..\GTFS-METRO-MEDELLIN"
"""

import argparse
import os
import sys
from datetime import date
from pathlib import Path

import pandas as pd
from google.cloud import bigquery, storage

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "metro-medellin-analytics")
BQ_DATASET = os.getenv("BQ_DATASET", "bronze")
GCS_BUCKET = os.getenv("GCS_BUCKET", "metro-medellin-raw")
GCS_PREFIX = f"gtfs/{date.today().isoformat()}"

SCHEMAS = {
    "agency": [
        bigquery.SchemaField("agency_id", "STRING"),
        bigquery.SchemaField("agency_name", "STRING"),
        bigquery.SchemaField("agency_url", "STRING"),
        bigquery.SchemaField("agency_timezone", "STRING"),
        bigquery.SchemaField("agency_lang", "STRING"),
        bigquery.SchemaField("agency_phone", "STRING"),
    ],
    "routes": [
        bigquery.SchemaField("route_id", "STRING"),
        bigquery.SchemaField("agency_id", "STRING"),
        bigquery.SchemaField("route_short_name", "STRING"),
        bigquery.SchemaField("route_long_name", "STRING"),
        bigquery.SchemaField("route_desc", "STRING"),
        bigquery.SchemaField("route_type", "INTEGER"),
        bigquery.SchemaField("route_url", "STRING"),
        bigquery.SchemaField("route_color", "STRING"),
        bigquery.SchemaField("route_text_color", "STRING"),
    ],
    "stops": [
        bigquery.SchemaField("stop_id", "STRING"),
        bigquery.SchemaField("stop_code", "STRING"),
        bigquery.SchemaField("stop_name", "STRING"),
        bigquery.SchemaField("stop_desc", "STRING"),
        bigquery.SchemaField("stop_lat", "FLOAT64"),
        bigquery.SchemaField("stop_lon", "FLOAT64"),
        bigquery.SchemaField("zone_id", "STRING"),
        bigquery.SchemaField("stop_url", "STRING"),
        bigquery.SchemaField("location_type", "INTEGER"),
        bigquery.SchemaField("parent_station", "STRING"),
        bigquery.SchemaField("stop_timezone", "STRING"),
        bigquery.SchemaField("wheelchair_boarding", "INTEGER"),
    ],
    "trips": [
        bigquery.SchemaField("route_id", "STRING"),
        bigquery.SchemaField("service_id", "STRING"),
        bigquery.SchemaField("trip_id", "STRING"),
        bigquery.SchemaField("trip_headsign", "STRING"),
        bigquery.SchemaField("trip_short_name", "STRING"),
        bigquery.SchemaField("direction_id", "INTEGER"),
        bigquery.SchemaField("block_id", "STRING"),
        bigquery.SchemaField("shape_id", "STRING"),
    ],
    "calendar": [
        bigquery.SchemaField("service_id", "STRING"),
        bigquery.SchemaField("monday", "INTEGER"),
        bigquery.SchemaField("tuesday", "INTEGER"),
        bigquery.SchemaField("wednesday", "INTEGER"),
        bigquery.SchemaField("thursday", "INTEGER"),
        bigquery.SchemaField("friday", "INTEGER"),
        bigquery.SchemaField("saturday", "INTEGER"),
        bigquery.SchemaField("sunday", "INTEGER"),
        bigquery.SchemaField("start_date", "STRING"),
        bigquery.SchemaField("end_date", "STRING"),
    ],
    "calendar_dates": [
        bigquery.SchemaField("service_id", "STRING"),
        bigquery.SchemaField("date", "STRING"),
        bigquery.SchemaField("exception_type", "INTEGER"),
    ],
    "stop_times": [
        bigquery.SchemaField("trip_id", "STRING"),
        bigquery.SchemaField("arrival_time", "STRING"),
        bigquery.SchemaField("departure_time", "STRING"),
        bigquery.SchemaField("stop_id", "STRING"),
        bigquery.SchemaField("stop_sequence", "INTEGER"),
        bigquery.SchemaField("stop_headsign", "STRING"),
        bigquery.SchemaField("pickup_type", "INTEGER"),
        bigquery.SchemaField("drop_off_type", "INTEGER"),
        bigquery.SchemaField("shape_dist_traveled", "FLOAT64"),
    ],
    "shapes": [
        bigquery.SchemaField("shape_id", "STRING"),
        bigquery.SchemaField("shape_pt_lat", "FLOAT64"),
        bigquery.SchemaField("shape_pt_lon", "FLOAT64"),
        bigquery.SchemaField("shape_pt_sequence", "INTEGER"),
        bigquery.SchemaField("shape_dist_traveled", "FLOAT64"),
    ],
    "transfers": [
        bigquery.SchemaField("from_stop_id", "STRING"),
        bigquery.SchemaField("to_stop_id", "STRING"),
        bigquery.SchemaField("transfer_type", "INTEGER"),
        bigquery.SchemaField("min_transfer_time", "INTEGER"),
    ],
}

NUMERIC_COLS = {
    "routes": ["route_type"],
    "stops": ["stop_lat", "stop_lon", "location_type", "wheelchair_boarding"],
    "trips": ["direction_id"],
    "calendar": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
    "calendar_dates": ["exception_type"],
    "stop_times": ["stop_sequence", "pickup_type", "drop_off_type", "shape_dist_traveled"],
    "shapes": ["shape_pt_lat", "shape_pt_lon", "shape_pt_sequence", "shape_dist_traveled"],
    "transfers": ["transfer_type", "min_transfer_time"],
}


def upload_to_gcs(local_path, gcs_client):
    bucket = gcs_client.bucket(GCS_BUCKET)
    blob_name = f"{GCS_PREFIX}/{local_path.name}"
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(str(local_path))
    uri = f"gs://{GCS_BUCKET}/{blob_name}"
    print(f"  GCS ok  {uri}")
    return uri


def load_to_bigquery(table_name, df, bq_client):
    table_ref = f"{PROJECT_ID}.{BQ_DATASET}.{table_name}"
    schema = SCHEMAS[table_name]
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    rows = bq_client.get_table(table_ref).num_rows
    print(f"  BQ  ok  {table_ref}  ({rows:,} filas)")
    return rows


def read_gtfs_file(path, table_name):
    df = pd.read_csv(path, dtype=str, keep_default_na=False, skipinitialspace=True)
    df = df.dropna(how="all")
    df = df[df.apply(lambda r: r.str.strip().ne("").any(), axis=1)]
    df.columns = [c.strip().lstrip("﻿") for c in df.columns]
    for col in NUMERIC_COLS.get(table_name, []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace("", None), errors="coerce")
    return df


def main(gtfs_dir):
    gtfs_path = Path(gtfs_dir).resolve()
    if not gtfs_path.exists():
        print(f"ERROR: No se encontro el directorio GTFS: {gtfs_path}", file=sys.stderr)
        sys.exit(1)

    print(f"\nProyecto GCP : {PROJECT_ID}")
    print(f"Bucket GCS   : gs://{GCS_BUCKET}/{GCS_PREFIX}/")
    print(f"Dataset BQ   : {BQ_DATASET}\n")

    gcs_client = storage.Client(project=PROJECT_ID)
    bq_client = bigquery.Client(project=PROJECT_ID)

    total_rows = 0
    errores = []

    for table_name in SCHEMAS:
        file_path = gtfs_path / f"{table_name}.txt"
        if not file_path.exists():
            print(f"  SKIP {table_name}.txt (no encontrado)")
            continue

        print(f"\n[{table_name}]")
        try:
            df = read_gtfs_file(file_path, table_name)
            print(f"  CSV ok  {len(df):,} filas leidas")
            upload_to_gcs(file_path, gcs_client)
            rows = load_to_bigquery(table_name, df, bq_client)
            total_rows += rows
        except Exception as exc:
            print(f"  ERROR en {table_name}: {exc}", file=sys.stderr)
            errores.append(table_name)

    print(f"\n{'='*50}")
    print(f"Ingesta completada: {len(SCHEMAS) - len(errores)}/{len(SCHEMAS)} tablas")
    print(f"Total filas en BigQuery: {total_rows:,}")
    if errores:
        print(f"Tablas con error: {errores}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Carga GTFS -> GCS -> BigQuery bronze")
    parser.add_argument("--gtfs-dir", required=True, help="Ruta al directorio con archivos GTFS (.txt)")
    args = parser.parse_args()
    main(args.gtfs_dir)
