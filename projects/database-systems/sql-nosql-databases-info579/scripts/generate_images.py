#!/usr/bin/env python3
"""
generate_images.py — Visualization generator for the INFO 579 portfolio project.

Produces:
  images/er_diagram.png              - 8 base tables + FK relationships
  images/top_conditions.png          - Top 10 conditions by patient count
  images/top_procedures.png          - Top 10 procedures by volume
  images/top_providers.png           - Top 10 providers by encounter count
  images/coverage_distribution.png   - Patient coverage tier breakdown

Prerequisites
-------------
- graphviz Python library + Graphviz binaries (dot at /opt/homebrew/bin/dot)
- matplotlib, pandas
- MySQL 8+ running with data already loaded via load_csvs.py

Usage examples
--------------
# Full run (ER diagram + all charts):
    python scripts/generate_images.py --user matthewqthompson --database Final_Project

# Password from environment variable:
    export MYSQL_PASSWORD="TempPass2026!"
    python scripts/generate_images.py --user matthewqthompson --database Final_Project

# ER diagram only (no DB needed):
    python scripts/generate_images.py --er-only
"""

import argparse
import getpass
import os
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root — works regardless of cwd
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
IMAGES_DIR = PROJECT_ROOT / "images"


# ---------------------------------------------------------------------------
# ER Diagram
# ---------------------------------------------------------------------------

def generate_er_diagram(output_path: Path) -> None:
    """Render the 8 base tables and their FK relationships as a PNG ER diagram.

    Uses the graphviz Python library with the dot engine. Each table is
    rendered as an HTML-like record node showing table name + key columns.
    FK edges are drawn as directed arrows from child column to parent PK.
    """
    try:
        import graphviz  # type: ignore[import-not-found]
    except ImportError:
        print("  ERROR: 'graphviz' Python package not installed. Run: pip install graphviz")
        sys.exit(1)

    dot = graphviz.Digraph(
        name="ER_Diagram",
        comment="INFO 579 Final Project — Base Tables",
        format="png",
        engine="dot",
    )

    dot.attr(
        rankdir="LR",
        bgcolor="white",
        fontname="Helvetica",
        fontsize="11",
        nodesep="1.0",
        ranksep="2.5",
        splines="ortho",  # orthogonal edges, with compass-direction ports
                          # below to keep them outside table boundaries
        concentrate="true",  # merge parallel edges going to the same target
        # Point to the Homebrew-installed dot binary
        # (graphviz library respects PATH; we also set it explicitly below)
    )
    dot.attr("node", shape="none", margin="0", fontname="Helvetica", fontsize="10")
    dot.attr("edge", fontname="Helvetica", fontsize="9", color="#555555")

    # ------------------------------------------------------------------
    # Color palette
    # ------------------------------------------------------------------
    HEADER_BG  = "#2C5F8A"   # dark blue header
    HEADER_FG  = "white"
    ROW_BG     = "#EAF3FB"   # light blue rows
    ALT_BG     = "#FFFFFF"   # alternating white
    BORDER     = "#2C5F8A"

    def _table_html(
        table_name: str,
        columns: list[tuple[str, str]],   # [(col_name, type_hint), ...]
    ) -> str:
        """Build an HTML-like label string for a record node."""
        header = (
            f'<TR><TD COLSPAN="2" BGCOLOR="{HEADER_BG}" ALIGN="CENTER">'
            f'<FONT COLOR="{HEADER_FG}"><B>{table_name}</B></FONT></TD></TR>'
        )
        rows_html = []
        for i, (col, hint) in enumerate(columns):
            bg = ROW_BG if i % 2 == 0 else ALT_BG
            row = (
                f'<TR>'
                f'<TD BGCOLOR="{bg}" ALIGN="LEFT" PORT="{col}">'
                f'<FONT COLOR="#1A1A1A">{col}</FONT></TD>'
                f'<TD BGCOLOR="{bg}" ALIGN="LEFT">'
                f'<FONT COLOR="#555555"><I>{hint}</I></FONT></TD>'
                f'</TR>'
            )
            rows_html.append(row)
        all_rows = "\n".join(rows_html)
        return (
            f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" '
            f'CELLPADDING="4" BGCOLOR="white" COLOR="{BORDER}">'
            f'{header}'
            f'{all_rows}'
            f'</TABLE>>'
        )

    # ------------------------------------------------------------------
    # Table definitions: (table_name, [(col_name, type_hint), ...])
    # Only key / representative columns shown (4-6 per table).
    # ------------------------------------------------------------------
    tables: dict[str, list[tuple[str, str]]] = {
        "patient": [
            ("patient_id",         "PK · varchar(36)"),
            ("first_name",         "varchar(20)"),
            ("last_name",          "varchar(20)"),
            ("birth_date",         "date"),
            ("healthcare_coverage","decimal(12,2)"),
            ("patient_state",      "varchar(20)"),
        ],
        "provider": [
            ("provider_id",       "PK · varchar(36)"),
            ("organization_id",   "varchar(36)"),
            ("provider_name",     "varchar(30)"),
            ("provider_specialty","varchar(50)"),
            ("provider_state",    "varchar(20)"),
            ("utilization",       "int"),
        ],
        "encounter": [
            ("encounter_id",           "PK · varchar(36)"),
            ("patient_id",             "FK → patient"),
            ("provider_id",            "FK → provider"),
            ("organization_id",        "FK → provider"),
            ("encounter_class",        "varchar(50)"),
            ("encounter_start_date",   "datetime"),
        ],
        "medical_condition": [
            ("condition_id",          "PK · bigint AUTO"),
            ("patient_id",            "FK → patient"),
            ("encounter_id",          "FK → encounter"),
            ("condition_code",        "varchar(36)"),
            ("condition_description", "varchar(255)"),
            ("condition_start_date",  "date"),
        ],
        "diagnosis": [
            ("patient_id",   "PK · FK → patient"),
            ("condition_id", "PK · FK → medical_condition"),
        ],
        "procedures": [
            ("procedure_id",          "PK · bigint AUTO"),
            ("patient_id",            "FK → patient"),
            ("encounter_id",          "FK → encounter"),
            ("procedure_code",        "varchar(36)"),
            ("procedure_description", "varchar(255)"),
            ("procedure_base_cost",   "decimal(12,2)"),
        ],
        "treatment": [
            ("patient_id",   "PK · FK → patient"),
            ("procedure_id", "PK · FK → procedures"),
        ],
        "observation": [
            ("observation_id",    "PK · bigint AUTO"),
            ("patient_id",        "FK → patient"),
            ("encounter_id",      "FK → encounter"),
            ("observation_code",  "varchar(36)"),
            ("observation_desc",  "varchar(255)"),
            ("observation_value", "varchar(255)"),
        ],
    }

    # Add nodes
    for tbl, cols in tables.items():
        dot.node(tbl, label=_table_html(tbl, cols))

    # ------------------------------------------------------------------
    # FK edges: (child_table:child_port, parent_table:parent_port, label)
    # ------------------------------------------------------------------
    # Compass-direction ports (`:e` exit east, `:w` enter west) force
    # graphviz to route edges from table boundaries rather than through
    # the middle of tables, avoiding the overlap issue.
    edges: list[tuple[str, str, str]] = [
        # encounter → patient
        ("encounter:patient_id:e",             "patient:patient_id:w",         ""),
        # encounter → provider (composite)
        ("encounter:provider_id:e",            "provider:provider_id:w",       "(provider_id, org_id)"),
        # medical_condition → patient
        ("medical_condition:patient_id:e",     "patient:patient_id:w",         ""),
        # medical_condition → encounter
        ("medical_condition:encounter_id:e",   "encounter:encounter_id:w",     ""),
        # diagnosis → patient
        ("diagnosis:patient_id:e",             "patient:patient_id:w",         ""),
        # diagnosis → medical_condition
        ("diagnosis:condition_id:e",           "medical_condition:condition_id:w", ""),
        # procedures → patient
        ("procedures:patient_id:e",            "patient:patient_id:w",         ""),
        # procedures → encounter
        ("procedures:encounter_id:e",          "encounter:encounter_id:w",     ""),
        # treatment → patient
        ("treatment:patient_id:e",             "patient:patient_id:w",         ""),
        # treatment → procedures
        ("treatment:procedure_id:e",           "procedures:procedure_id:w",    ""),
        # observation → patient
        ("observation:patient_id:e",           "patient:patient_id:w",         ""),
        # observation → encounter
        ("observation:encounter_id:e",         "encounter:encounter_id:w",     ""),
    ]

    for child_port, parent_port, label in edges:
        # Use xlabel (external label) instead of label — ortho splines
        # don't render mid-line labels properly. xlabel floats freely.
        dot.edge(
            child_port,
            parent_port,
            xlabel=label,
            arrowhead="normal",
            arrowtail="none",
            color="#2C5F8A",
            penwidth="1.2",
        )

    # Render — graphviz uses PATH, but we also hint the Homebrew bin
    env_path = os.environ.get("PATH", "")
    homebrew_bin = "/opt/homebrew/bin"
    if homebrew_bin not in env_path:
        os.environ["PATH"] = f"{homebrew_bin}:{env_path}"

    # graphviz.render() or dot.render() writes <stem>.png
    # We pass the output directory; graphviz appends ".png"
    stem = str(output_path.with_suffix(""))
    dot.render(filename=stem, cleanup=True)

    # graphviz names the file <stem>.png — nothing else to do
    print(f"  Saved: {output_path}")


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------

def _apply_chart_style() -> None:
    """Apply the shared matplotlib style used across all charts."""
    import matplotlib.pyplot as plt  # type: ignore[import-not-found]

    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        # Older matplotlib versions name the style without the version suffix
        try:
            plt.style.use("seaborn-whitegrid")
        except OSError:
            pass  # Fall back to default if neither is available


def _save_fig(fig, output_path: Path) -> None:
    """Save figure to PNG at 150 DPI with tight layout."""
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  Saved: {output_path}")


def _fmt_count(n: int) -> str:
    """Format an integer with thousands separator."""
    return f"{n:,}"


# ---------------------------------------------------------------------------
# Chart generators
# ---------------------------------------------------------------------------

def generate_top_conditions(conn, output_path: Path) -> None:
    """Horizontal bar chart — top 10 conditions by distinct patient count."""
    import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    import matplotlib.ticker as mticker  # type: ignore[import-not-found]

    query = textwrap.dedent("""
        SELECT condition_description, COUNT(DISTINCT patient_id) AS n_patients
        FROM medical_condition
        GROUP BY condition_description
        ORDER BY n_patients DESC
        LIMIT 10
    """).strip()

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        print("  WARNING: No data returned for top_conditions. Skipping chart.")
        return

    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]

    # Reverse so the largest bar is at the top
    labels = labels[::-1]
    values = values[::-1]

    _apply_chart_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(
        labels, values,
        color="#4682B4",
        edgecolor="white",
        linewidth=0.5,
        height=0.65,
    )

    # Annotate bars with count
    for bar, v in zip(bars, values):
        ax.text(
            bar.get_width() + max(values) * 0.005,
            bar.get_y() + bar.get_height() / 2,
            _fmt_count(v),
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlabel("Number of Patients", fontsize=11, labelpad=8)
    ax.set_title("Top 10 Conditions by Patient Count", fontsize=14, fontweight="bold", pad=14)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlim(0, max(values) * 1.12)
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)

    # Trim long labels so the chart stays readable
    wrapped = [textwrap.fill(lbl, width=45) for lbl in labels]
    ax.set_yticklabels(wrapped)

    fig.tight_layout()
    _save_fig(fig, output_path)
    plt.close(fig)


def generate_top_procedures(conn, output_path: Path) -> None:
    """Horizontal bar chart — top 10 procedures by total volume."""
    import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    import matplotlib.ticker as mticker  # type: ignore[import-not-found]

    query = textwrap.dedent("""
        SELECT procedure_description, COUNT(*) AS n_procedures
        FROM procedures
        GROUP BY procedure_description
        ORDER BY n_procedures DESC
        LIMIT 10
    """).strip()

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        print("  WARNING: No data returned for top_procedures. Skipping chart.")
        return

    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]

    labels = labels[::-1]
    values = values[::-1]

    _apply_chart_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(
        labels, values,
        color="#2E8B57",
        edgecolor="white",
        linewidth=0.5,
        height=0.65,
    )

    for bar, v in zip(bars, values):
        ax.text(
            bar.get_width() + max(values) * 0.005,
            bar.get_y() + bar.get_height() / 2,
            _fmt_count(v),
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlabel("Number of Procedures", fontsize=11, labelpad=8)
    ax.set_title("Top 10 Procedures by Volume", fontsize=14, fontweight="bold", pad=14)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlim(0, max(values) * 1.12)
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)

    wrapped = [textwrap.fill(lbl, width=45) for lbl in labels]
    ax.set_yticklabels(wrapped)

    fig.tight_layout()
    _save_fig(fig, output_path)
    plt.close(fig)


def generate_top_providers(conn, output_path: Path) -> None:
    """Horizontal bar chart — top 10 providers by encounter count from rpt_provider_utilization."""
    import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    import matplotlib.ticker as mticker  # type: ignore[import-not-found]

    query = textwrap.dedent("""
        SELECT CONCAT(provider_name, ' (', provider_specialty, ')') AS provider_label,
               n_encounters
        FROM rpt_provider_utilization
        ORDER BY n_encounters DESC
        LIMIT 10
    """).strip()

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        print("  WARNING: No data returned for top_providers. Skipping chart.")
        return

    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]

    labels = labels[::-1]
    values = values[::-1]

    _apply_chart_style()
    fig, ax = plt.subplots(figsize=(13, 7))

    bars = ax.barh(
        labels, values,
        color="#6A5ACD",
        edgecolor="white",
        linewidth=0.5,
        height=0.65,
    )

    for bar, v in zip(bars, values):
        ax.text(
            bar.get_width() + max(values) * 0.005,
            bar.get_y() + bar.get_height() / 2,
            _fmt_count(v),
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlabel("Number of Encounters", fontsize=11, labelpad=8)
    ax.set_title("Top 10 Providers by Encounter Volume", fontsize=14, fontweight="bold", pad=14)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlim(0, max(values) * 1.12)
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)

    wrapped = [textwrap.fill(lbl, width=50) for lbl in labels]
    ax.set_yticklabels(wrapped)

    fig.tight_layout()
    _save_fig(fig, output_path)
    plt.close(fig)


def generate_coverage_distribution(conn, output_path: Path) -> None:
    """Vertical bar chart — patient count by healthcare coverage tier (high/medium/low)."""
    import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    import matplotlib.ticker as mticker  # type: ignore[import-not-found]

    query = textwrap.dedent("""
        SELECT
          SUM(CASE WHEN healthcare_coverage >= 10000 THEN 1 ELSE 0 END)                                    AS high_coverage,
          SUM(CASE WHEN healthcare_coverage >= 5000 AND healthcare_coverage < 10000 THEN 1 ELSE 0 END)     AS medium_coverage,
          SUM(CASE WHEN healthcare_coverage < 5000 THEN 1 ELSE 0 END)                                      AS low_coverage
        FROM patient
    """).strip()

    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()

    if not row or row[0] is None:
        print("  WARNING: No data returned for coverage_distribution. Skipping chart.")
        return

    high_n, med_n, low_n = int(row[0] or 0), int(row[1] or 0), int(row[2] or 0)

    tiers   = ["High\n(≥$10K)", "Medium\n($5K–$10K)", "Low\n(<$5K)"]
    counts  = [high_n, med_n, low_n]
    colors  = ["#3A9E63", "#4682B4", "#888888"]   # green, blue, gray

    _apply_chart_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.bar(
        tiers, counts,
        color=colors,
        edgecolor="white",
        linewidth=0.8,
        width=0.5,
    )

    # Annotate bars with count on top
    for bar, v in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(counts) * 0.015,
            _fmt_count(v),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#333333",
        )

    ax.set_ylabel("Number of Patients", fontsize=11, labelpad=8)
    ax.set_title("Patient Healthcare Coverage Distribution", fontsize=14, fontweight="bold", pad=14)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_ylim(0, max(counts) * 1.15)
    ax.tick_params(axis="x", labelsize=11)
    ax.tick_params(axis="y", labelsize=9)

    fig.tight_layout()
    _save_fig(fig, output_path)
    plt.close(fig)


# ---------------------------------------------------------------------------
# DB connection
# ---------------------------------------------------------------------------

def connect_db(args: argparse.Namespace):
    """Connect to MySQL and return the connection object, or None on failure."""
    try:
        import mysql.connector  # type: ignore[import-not-found]
    except ImportError:
        print("  WARNING: mysql-connector-python not installed. Charts will be skipped.")
        return None

    password = args.password
    if password is None:
        try:
            password = getpass.getpass(f"MySQL password for {args.user}@{args.host}: ")
        except (KeyboardInterrupt, EOFError):
            print("\nPassword entry cancelled. Charts will be skipped.")
            return None

    try:
        conn = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=password,
            database=args.database,
            charset="utf8mb4",
            use_pure=True,
            connection_timeout=30,
        )
        return conn
    except mysql.connector.Error as exc:
        print(f"  WARNING: Could not connect to MySQL: {exc}")
        print("  Charts will be skipped. ER diagram will still be generated.")
        return None


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate PNG visualizations for the INFO 579 portfolio project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              python scripts/generate_images.py --user matthewqthompson --database Final_Project
              MYSQL_PASSWORD=secret python scripts/generate_images.py --user root
              python scripts/generate_images.py --er-only
        """),
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="MySQL host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        default=3306,
        type=int,
        help="MySQL port (default: 3306)",
    )
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
        "--er-only",
        action="store_true",
        help="Generate only the ER diagram, skip all charts (no DB connection needed)",
    )
    parser.add_argument(
        "--regen-er",
        action="store_true",
        help="Force-regenerate the ER diagram via graphviz, overwriting the hand-curated images/er_diagram.png",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Directory where PNG files will be written "
            "(default: images/ at the project root)"
        ),
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # Resolve output directory
    if args.output_dir is not None:
        images_dir = Path(args.output_dir).resolve()
    else:
        images_dir = IMAGES_DIR

    images_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {images_dir}\n")

    # --- ER Diagram (no DB needed) ---
    # The ER diagram in images/er_diagram.png is a hand-curated screenshot
    # from a database modeling tool (cleaner than what graphviz produces
    # for this many tables). Only regenerate via graphviz when explicitly
    # asked with --regen-er, or if the file is missing.
    er_path = images_dir / "er_diagram.png"
    if args.regen_er or not er_path.exists():
        print("Generating ER diagram (graphviz)...")
        try:
            generate_er_diagram(er_path)
            print("  Done. ✓")
        except Exception as exc:
            print(f"  ERROR generating ER diagram: {exc}")
    else:
        print("Skipping ER diagram (using existing hand-curated images/er_diagram.png; pass --regen-er to overwrite).")

    if args.er_only:
        print("\nDone (--er-only mode; charts skipped).")
        return

    # --- DB connection ---
    print("\nConnecting to database...")
    conn = connect_db(args)

    if conn is None:
        print("\nSkipping all charts due to missing DB connection.")
        return

    print("  Connected. ✓\n")

    chart_tasks = [
        (
            "top_conditions",
            images_dir / "top_conditions.png",
            generate_top_conditions,
        ),
        (
            "top_procedures",
            images_dir / "top_procedures.png",
            generate_top_procedures,
        ),
        (
            "top_providers",
            images_dir / "top_providers.png",
            generate_top_providers,
        ),
        (
            "coverage_distribution",
            images_dir / "coverage_distribution.png",
            generate_coverage_distribution,
        ),
    ]

    for chart_name, out_path, fn in chart_tasks:
        print(f"Generating {chart_name} chart...")
        try:
            fn(conn, out_path)
            print("  Done. ✓")
        except Exception as exc:
            print(f"  ERROR generating {chart_name}: {exc}")

    conn.close()
    print("\nAll images generated.")


if __name__ == "__main__":
    main()
