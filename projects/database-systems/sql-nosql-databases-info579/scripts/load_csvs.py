#!/usr/bin/env python3
"""
load_csvs.py — Synthea CSV → MySQL loader for the INFO579 Final_Project database.

Reads 6 Synthea-generated CSV files from the project's data/ directory and
populates 8 base tables in the correct FK-dependency order. The two junction
tables (diagnosis, treatment) are derived from already-inserted rows rather
than from a CSV.

Prerequisites
-------------
- MySQL 8+ running with the Final_Project schema already created
  (run sql/00_schema.sql first)
- Python 3.9+
- pip install -r requirements.txt   (pandas, mysql-connector-python)

Usage examples
--------------
# Using environment variables (recommended for CI / shared machines):
    export MYSQL_USER=root
    export MYSQL_PASSWORD=secret
    python scripts/load_csvs.py

# Using CLI flags:
    python scripts/load_csvs.py --host 127.0.0.1 --port 3306 \\
        --user root --password secret --database Final_Project

# Interactive password prompt (nothing stored on disk):
    python scripts/load_csvs.py --user root

# Append-only mode (skip TRUNCATE, add rows to whatever is already there):
    python scripts/load_csvs.py --no-truncate

# Custom data directory:
    python scripts/load_csvs.py --data-dir /path/to/synthea/output/csv
"""

import argparse
import getpass
import os
import sys
import time
from pathlib import Path
from typing import Optional

import mysql.connector  # type: ignore[import-not-found]
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BATCH_SIZE = 1_000

# Ordered list of (table_name, csv_filename_or_None)
# None means the table is populated from SQL, not a CSV.
TABLE_LOAD_ORDER: list[tuple[str, Optional[str]]] = [
    ("patient",           "patients.csv"),
    ("provider",          "providers.csv"),
    ("encounter",         "encounters.csv"),
    ("medical_condition", "conditions.csv"),
    ("procedures",        "procedures.csv"),
    ("observation",       "observations.csv"),
    ("diagnosis",         None),  # derived from medical_condition
    ("treatment",         None),  # derived from procedures
]

# ---------------------------------------------------------------------------
# Column mappings: {schema_column: csv_column}
# ---------------------------------------------------------------------------

PATIENT_COLS: dict[str, str] = {
    "patient_id":            "Id",
    "birth_date":            "BIRTHDATE",
    "death_date":            "DEATHDATE",
    "ssn":                   "SSN",
    "driver_license_number": "DRIVERS",
    "passport_number":       "PASSPORT",
    "prefix":                "PREFIX",
    "first_name":            "FIRST",
    "last_name":             "LAST",
    "suffix":                "SUFFIX",
    "maiden_name":           "MAIDEN",
    "marital_status":        "MARITAL",
    "patient_race":          "RACE",
    "patient_ethnicity":     "ETHNICITY",
    "patient_gender":        "GENDER",
    "birth_place":           "BIRTHPLACE",
    "patient_address":       "ADDRESS",
    "patient_city":          "CITY",
    "patient_state":         "STATE",
    "patient_county":        "COUNTY",
    "patient_zip_code":      "ZIP",
    "patient_latitude":      "LAT",
    "patient_longitude":     "LON",
    "healthcare_expenses":   "HEALTHCARE_EXPENSES",
    "healthcare_coverage":   "HEALTHCARE_COVERAGE",
}

PROVIDER_COLS: dict[str, str] = {
    "provider_id":        "Id",
    "organization_id":    "ORGANIZATION",
    "provider_name":      "NAME",
    "provider_gender":    "GENDER",
    "provider_specialty": "SPECIALITY",
    "provider_address":   "ADDRESS",
    "provider_city":      "CITY",
    "provider_state":     "STATE",
    "provider_zip_code":  "ZIP",
    "provider_latitude":  "LAT",
    "provider_longitude": "LON",
    "utilization":        "UTILIZATION",
}

ENCOUNTER_COLS: dict[str, str] = {
    "encounter_id":                  "Id",
    "patient_id":                    "PATIENT",
    "provider_id":                   "PROVIDER",
    "organization_id":               "ORGANIZATION",
    "encounter_start_date":          "START",
    "encounter_end_date":            "STOP",
    "payer_uuid":                    "PAYER",
    "encounter_class":               "ENCOUNTERCLASS",
    "encounter_code":                "CODE",
    "encounter_description":         "DESCRIPTION",
    "base_encounter_cost":           "BASE_ENCOUNTER_COST",
    "total_claim_cost":              "TOTAL_CLAIM_COST",
    "payer_coverage":                "PAYER_COVERAGE",
    "encounter_reason_code":         "REASONCODE",
    "encounter_reason_description":  "REASONDESCRIPTION",
}

MEDICAL_CONDITION_COLS: dict[str, str] = {
    # condition_id is AUTO_INCREMENT — omit it entirely
    "condition_start_date": "START",
    "condition_end_date":   "STOP",
    "patient_id":           "PATIENT",
    "encounter_id":         "ENCOUNTER",
    "condition_code":       "CODE",
    "condition_description":"DESCRIPTION",
}

PROCEDURES_COLS: dict[str, str] = {
    # procedure_id is AUTO_INCREMENT — omit it entirely
    "procedure_date":              "DATE",
    "patient_id":                  "PATIENT",
    "encounter_id":                "ENCOUNTER",
    "procedure_code":              "CODE",
    "procedure_description":       "DESCRIPTION",
    "procedure_base_cost":         "BASE_COST",
    "procedure_reason_code":       "REASONCODE",
    "procedure_reason_description":"REASONDESCRIPTION",
}

OBSERVATION_COLS: dict[str, str] = {
    # observation_id is AUTO_INCREMENT — omit it entirely
    "observation_date":  "DATE",
    "patient_id":        "PATIENT",
    "encounter_id":      "ENCOUNTER",
    "observation_code":  "CODE",
    "observation_desc":  "DESCRIPTION",
    "observation_value": "VALUE",
    "observation_units": "UNITS",
    "observation_type":  "TYPE",
}

TABLE_COL_MAP: dict[str, dict[str, str]] = {
    "patient":           PATIENT_COLS,
    "provider":          PROVIDER_COLS,
    "encounter":         ENCOUNTER_COLS,
    "medical_condition": MEDICAL_CONDITION_COLS,
    "procedures":        PROCEDURES_COLS,
    "observation":       OBSERVATION_COLS,
}

# SQL for junction tables derived from base tables
DERIVED_SQL: dict[str, str] = {
    "diagnosis": (
        "INSERT INTO diagnosis (patient_id, condition_id) "
        "SELECT DISTINCT patient_id, condition_id FROM medical_condition"
    ),
    "treatment": (
        "INSERT INTO treatment (patient_id, procedure_id) "
        "SELECT DISTINCT patient_id, procedure_id FROM procedures"
    ),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def nan_to_none(value: object) -> object:
    """Convert pandas NaN / float('nan') to Python None for MySQL NULL."""
    if value is None:
        return None
    try:
        import math
        if isinstance(value, float) and math.isnan(value):
            return None
    except (TypeError, ValueError):
        pass
    # pandas NA check (works on pd.NA and np.nan alike).
    # pd.isna returns a scalar bool for scalar input, but Pyright sees the
    # broader return type — narrow with isinstance(..., bool).
    try:
        is_na = pd.isna(value)
        if isinstance(is_na, bool) and is_na:
            return None
    except (TypeError, ValueError):
        pass
    return value


def clean_row(row: dict) -> tuple:
    """Return a tuple of values with NaN replaced by None."""
    return tuple(nan_to_none(v) for v in row.values())


def build_insert_sql(table: str, columns: list[str]) -> str:
    """Build a parameterized INSERT statement for executemany()."""
    col_list = ", ".join(f"`{c}`" for c in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    return f"INSERT INTO `{table}` ({col_list}) VALUES ({placeholders})"


def truncate_table(cursor: mysql.connector.cursor.MySQLCursor, table: str) -> None:
    """Truncate a single table with FK checks disabled."""
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute(f"TRUNCATE TABLE `{table}`")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def row_count(cursor: mysql.connector.cursor.MySQLCursor, table: str) -> int:
    """Return the current row count for a table."""
    cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
    result = cursor.fetchone()
    return result[0] if result else 0


def load_csv_table(
    conn: mysql.connector.connection.MySQLConnection,
    table: str,
    csv_path: Path,
    col_map: dict[str, str],
    truncate: bool,
    step_num: int,
    total_steps: int,
) -> int:
    """
    Load one CSV file into one table.

    Returns the number of rows inserted.
    Raises RuntimeError on hard failures.
    """
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False, na_values=[""])
    # Remap CSV columns to schema columns
    reverse_map = {csv_col: schema_col for schema_col, csv_col in col_map.items()}
    # Only keep columns we care about (some CSVs have extra columns)
    available = [c for c in df.columns if c in reverse_map]
    missing_csv_cols = [csv_col for csv_col in col_map.values() if csv_col not in df.columns]
    if missing_csv_cols:
        # Warn but don't crash — Synthea versions can differ slightly
        print(
            f"  WARNING: {csv_path.name} missing expected CSV columns: {missing_csv_cols}. "
            "Affected schema columns will be omitted (check for nullability)."
        )

    # Subset to relevant CSV columns, then rename to schema column names.
    # (Using direct column assignment rather than .rename() to sidestep
    # a pandas-stubs overload-resolution quirk with dict[str, str] arg.)
    df = df[available].copy()
    df.columns = pd.Index([reverse_map[c] for c in df.columns])
    schema_cols = list(df.columns)
    n_rows = len(df)

    print(f"[{step_num}/{total_steps}] Loading {table} ({n_rows:,} rows)...", end=" ", flush=True)
    t0 = time.perf_counter()

    cursor = conn.cursor()
    try:
        if truncate:
            truncate_table(cursor, table)
            conn.commit()

        insert_sql = build_insert_sql(table, schema_cols)

        # Batch insert
        batch: list[tuple] = []
        fk_warning_count = 0
        rows_inserted = 0

        for _, row in df.iterrows():
            batch.append(clean_row(row.to_dict()))
            if len(batch) >= BATCH_SIZE:
                fk_warning_count, rows_inserted = _execute_batch(
                    cursor, conn, insert_sql, batch,
                    fk_warning_count, rows_inserted
                )
                batch = []

        if batch:
            fk_warning_count, rows_inserted = _execute_batch(
                cursor, conn, insert_sql, batch,
                fk_warning_count, rows_inserted
            )

        conn.commit()
        elapsed = time.perf_counter() - t0

        if fk_warning_count:
            print(
                f"done in {elapsed:.1f}s  "
                f"(WARNING: {fk_warning_count} rows skipped — FK violation)"
            )
        else:
            print(f"done in {elapsed:.1f}s")

    except Exception as exc:
        conn.rollback()
        cursor.close()
        raise RuntimeError(f"Failed loading {table}: {exc}") from exc

    cursor.close()
    return rows_inserted


def _execute_batch(
    cursor: mysql.connector.cursor.MySQLCursor,
    conn: mysql.connector.connection.MySQLConnection,
    sql: str,
    batch: list[tuple],
    fk_warning_count: int,
    rows_inserted: int,
) -> tuple[int, int]:
    """
    Execute one batch with executemany().

    Falls back row-by-row on IntegrityError so a single bad FK reference
    doesn't abort the whole load. Returns updated (fk_warning_count, rows_inserted).
    """
    try:
        cursor.executemany(sql, batch)
        rows_inserted += len(batch)
    except mysql.connector.errors.IntegrityError:
        # Retry row-by-row so good rows still land
        conn.rollback()
        for row_tuple in batch:
            try:
                cursor.execute(sql, row_tuple)
                rows_inserted += 1
            except mysql.connector.errors.IntegrityError:
                fk_warning_count += 1
        conn.commit()
    return fk_warning_count, rows_inserted


def load_derived_table(
    conn: mysql.connector.connection.MySQLConnection,
    table: str,
    sql: str,
    truncate: bool,
    step_num: int,
    total_steps: int,
) -> int:
    """
    Populate a junction table from an existing base table via INSERT ... SELECT.

    Returns the number of rows inserted.
    """
    print(f"[{step_num}/{total_steps}] Deriving {table}...", end=" ", flush=True)
    t0 = time.perf_counter()
    cursor = conn.cursor()
    try:
        if truncate:
            truncate_table(cursor, table)
            conn.commit()
        cursor.execute(sql)
        rows_inserted = cursor.rowcount
        conn.commit()
        elapsed = time.perf_counter() - t0
        print(f"{rows_inserted:,} rows done in {elapsed:.1f}s")
    except Exception as exc:
        conn.rollback()
        cursor.close()
        raise RuntimeError(f"Failed deriving {table}: {exc}") from exc
    cursor.close()
    return rows_inserted


def print_summary(
    conn: mysql.connector.connection.MySQLConnection,
    table_order: list[str],
) -> None:
    """Print a final row-count summary for every loaded table."""
    cursor = conn.cursor()
    print("\n" + "=" * 45)
    print(f"{'Table':<22}  {'Row Count':>10}")
    print("-" * 45)
    for table in table_order:
        n = row_count(cursor, table)
        print(f"  {table:<20}  {n:>10,}")
    print("=" * 45)
    cursor.close()


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load Synthea CSV files into the Final_Project MySQL database.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--host",       default="127.0.0.1", help="MySQL host (default: 127.0.0.1)")
    parser.add_argument("--port",       default=3306, type=int, help="MySQL port (default: 3306)")
    parser.add_argument(
        "--user",
        default=os.environ.get("MYSQL_USER", "root"),
        help="MySQL user (default: $MYSQL_USER or root)",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("MYSQL_PASSWORD"),
        help="MySQL password (default: $MYSQL_PASSWORD; omit to prompt)",
    )
    parser.add_argument(
        "--database",
        default="Final_Project",
        help="Target database name (default: Final_Project)",
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Path to directory containing the Synthea CSV files (default: ../data relative to this script)",
    )
    parser.add_argument(
        "--no-truncate",
        action="store_true",
        help="Append rows instead of truncating tables before load (not idempotent)",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # Resolve data directory
    if args.data_dir is not None:
        data_dir = Path(args.data_dir).resolve()
    else:
        data_dir = (Path(__file__).parent.parent / "data").resolve()

    if not data_dir.is_dir():
        print(f"ERROR: data directory not found: {data_dir}", file=sys.stderr)
        sys.exit(1)

    # Resolve password
    password = args.password
    if password is None:
        password = getpass.getpass(f"MySQL password for {args.user}@{args.host}: ")

    truncate = not args.no_truncate
    if not truncate:
        print("NOTE: --no-truncate active — existing rows will NOT be cleared first.")

    # Connect
    print(f"\nConnecting to {args.user}@{args.host}:{args.port}/{args.database} ...")
    try:
        conn = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=password,
            database=args.database,
            charset="utf8mb4",
            use_pure=True,           # avoid C-extension issues on some platforms
            connection_timeout=30,
        )
    except mysql.connector.Error as exc:
        print(f"ERROR: could not connect to MySQL: {exc}", file=sys.stderr)
        sys.exit(1)

    print("Connected.\n")
    total_steps = len(TABLE_LOAD_ORDER)
    loaded_tables: list[str] = []

    for step, (table, csv_filename) in enumerate(TABLE_LOAD_ORDER, start=1):
        try:
            if csv_filename is not None:
                # CSV-backed table
                csv_path = data_dir / csv_filename
                if not csv_path.is_file():
                    print(
                        f"[{step}/{total_steps}] ERROR: CSV file not found: {csv_path}",
                        file=sys.stderr,
                    )
                    print("Aborting — subsequent tables depend on this one.", file=sys.stderr)
                    conn.close()
                    sys.exit(1)
                load_csv_table(
                    conn=conn,
                    table=table,
                    csv_path=csv_path,
                    col_map=TABLE_COL_MAP[table],
                    truncate=truncate,
                    step_num=step,
                    total_steps=total_steps,
                )
            else:
                # Derived junction table
                load_derived_table(
                    conn=conn,
                    table=table,
                    sql=DERIVED_SQL[table],
                    truncate=truncate,
                    step_num=step,
                    total_steps=total_steps,
                )
            loaded_tables.append(table)

        except RuntimeError as exc:
            print(f"\nERROR: {exc}", file=sys.stderr)
            print(
                "Aborting load — later tables have FK dependencies on this one.",
                file=sys.stderr,
            )
            conn.close()
            sys.exit(1)

    # Validation summary
    print_summary(conn, loaded_tables)
    conn.close()
    print("\nAll tables loaded successfully.")


if __name__ == "__main__":
    main()
