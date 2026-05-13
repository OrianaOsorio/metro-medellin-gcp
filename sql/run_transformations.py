"""
Ejecuta las transformaciones SQL de silver y gold en BigQuery.

Uso:
    python sql/run_transformations.py
    python sql/run_transformations.py --layer silver   # solo silver
    python sql/run_transformations.py --layer gold     # solo gold
"""

import argparse
import os
import time
from pathlib import Path

from google.cloud import bigquery

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "metro-medellin-analytics")

SQL_DIR = Path(__file__).parent

LAYERS = {
    "silver": sorted((SQL_DIR / "silver").glob("*.sql")),
    "gold":   sorted((SQL_DIR / "gold").glob("*.sql")),
    "ml":     sorted((SQL_DIR / "ml").glob("*.sql")),
}


def run_sql_file(path: Path, client: bigquery.Client) -> float:
    sql = path.read_text(encoding="utf-8-sig")  # utf-8-sig elimina BOM de archivos Windows
    t0 = time.time()
    job = client.query(sql)
    job.result()
    elapsed = time.time() - t0
    print(f"  ok  {path.name}  ({elapsed:.1f}s)")
    return elapsed


def main(layer: str) -> None:
    client = bigquery.Client(project=PROJECT_ID)

    layers_to_run = ["silver", "gold", "ml"] if layer == "all" else [layer]

    for lyr in layers_to_run:
        files = LAYERS[lyr]
        if not files:
            print(f"[{lyr}] Sin archivos SQL encontrados en sql/{lyr}/")
            continue

        print(f"\n[{lyr.upper()}] {len(files)} transformaciones")
        total = 0.0
        for sql_file in files:
            total += run_sql_file(sql_file, client)

        print(f"  Capa {lyr} completada en {total:.1f}s")

    print("\nTransformaciones finalizadas.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecuta SQL silver/gold en BigQuery")
    parser.add_argument(
        "--layer",
        choices=["silver", "gold", "ml", "all"],
        default="all",
        help="Capa a procesar (default: all)",
    )
    args = parser.parse_args()
    main(args.layer)
