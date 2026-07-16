[← Back to Database Systems Projects](../README.md)

# Healthcare Analytics with SQL

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](./reports/INFO579-Final-Project-Report-Thompson.pdf)
[![INFO 579](https://img.shields.io/badge/INFO%20579-SQL%20%26%20NoSQL-red?style=for-the-badge)](https://arizona.edu)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

> **Course project on database design and SQL analytics for healthcare data.** University of Arizona, INFO 579

**[View Full Report (PDF)](./reports/INFO579-Final-Project-Report-Thompson.pdf)** (8.1MB)

---

## Project Overview

Final project for INFO 579 (SQL & NoSQL Databases). The course covered both relational and document stores; this project focused on the SQL/relational track. I designed normalized database schemas and wrote complex SQL queries to analyze synthetic EHR data, building 9 fully documented analytical reports (plus 5 schema-defined) addressing clinical quality, provider utilization, readmissions, and profitability.

**Key Metrics**: 1,171 patients • 53,346 encounters • 8,376 conditions • 67MB Synthea EHR data

**Bottom line**: a reproducible, normalized MySQL warehouse over Synthea EHR data that turns raw records into operational analytics. For example, it surfaces a provider-workload imbalance (one GP handling 60%+ more encounters than any peer) and corrects a naive mortality metric into a defensible 30-day rate.

### Database Schema

The 8 base tables and their foreign-key relationships:

![ER diagram of base tables](./images/schema_er_diagram.png)

`diagnosis` and `treatment` are junction tables for the many-to-many relationships (patient ⇄ medical_condition, patient ⇄ procedures).

> Note: the diagram labels **`Condition`** and **`Procedure`** correspond to the SQL tables **`medical_condition`** and **`procedures`** (plural). The visual labels were shortened for readability; the actual schema uses the longer/plural names.

---

## What I Applied

### SQL Techniques

| Category              | Techniques                                                            |
| --------------------- | --------------------------------------------------------------------- |
| **Joins**             | Multi-table joins (up to 3 tables, incl. compound-key), LEFT/INNER      |
| **Temporal Analysis** | `DATE_ADD` (14-day follow-up window), `TIMESTAMPDIFF` (inpatient LOS)  |
| **Advanced Queries**  | CTEs (Common Table Expressions), correlated subqueries                |
| **Aggregation**       | `GROUP BY` + `HAVING`, `CASE` for categorization                      |
| **ETL**               | Batched parameterized `INSERT` (`executemany`), Pandas preprocessing   |

### Database Design

- **3NF Normalization**: 8 entity tables with 2 junction tables for many-to-many relationships
- **Foreign Keys**: 12 FK constraints with cascading relationships (patient→encounter→provider)
- **Schema Verified**: Record counts verified via AUTO_INCREMENT values in MySQL dump

### Business Insights

| Objective                | Key Finding                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| **Profitability**        | Top patient costs reached $1.1M; medication reconciliation, renal dialysis most common procedures |
| **Clinical Quality**     | Viral sinusitis most prevalent (63%); emergency 30-day mortality: 3.57/1,000 encounters           |
| **Provider Utilization** | Severe workload imbalance (top provider: 3,000+ encounters vs <2,000 for others)                  |
| **Readmissions**         | Flagged high-risk ER patients (≥3 visits) for intervention                                        |
| **Expansion**            | 5 inactive specialties identified for reallocation                                                |

---

## Healthcare Dataset

**6 Entities • 67MB Total • Synthea Synthetic EHR Data**

| Entity           | File                                          | Size  | Records | Description               |
| ---------------- | --------------------------------------------- | ----- | ------- | ------------------------- |
| **Patients**     | [`patients.csv`](./data/patients.csv)         | 325KB | 1,171   | Demographics, addresses   |
| **Encounters**   | [`encounters.csv`](./data/encounters.csv)     | 16MB  | 53,346  | Medical visits, billing   |
| **Conditions**   | [`conditions.csv`](./data/conditions.csv)     | 1MB   | 8,376   | ICD-10 diagnoses          |
| **Procedures**   | [`procedures.csv`](./data/procedures.csv)     | 5.7MB | 34,981  | CPT procedure codes       |
| **Observations** | [`observations.csv`](./data/observations.csv) | 43MB  | 299,697 | Lab results, vitals       |
| **Providers**    | [`providers.csv`](./data/providers.csv)       | 1MB   | 5,855   | Facilities, practitioners |

---

## Project Structure

```text
sql-nosql-databases-info579/
├── README.md                                          # Project documentation
├── docker-compose.yml                                 # MySQL 8 container (port 13306, auto-applies schema)
├── setup.sh                                           # One-command reproduction: docker + loader + reports
├── requirements.txt                                   # Python dependencies (pandas, mysql-connector-python, matplotlib)
├── relationship_verify.py                             # Pandas data-integrity check (pre-schema exploration)
├── scripts/
│   ├── load_csvs.py                                   # Synthea CSV → MySQL loader (8 tables, FK-ordered)
│   └── generate_charts.py                             # Regenerates the 4 analytical chart PNGs from DB data
├── images/                                            # PNGs embedded in this README
│   ├── schema_er_diagram.png
│   ├── top_conditions.png
│   ├── top_procedures.png
│   ├── top_providers.png
│   └── coverage_distribution.png
├── data/                                              # 6 healthcare CSVs (67MB total)
│   ├── patients.csv
│   ├── encounters.csv
│   ├── conditions.csv
│   ├── procedures.csv
│   ├── observations.csv
│   └── providers.csv
├── sql/
│   ├── 00_schema.sql                                  # 3NF schema: 8 base tables + 14 rpt_ tables + FK constraints
│   ├── analytical_reports/                            # Section 7: 6 analytical reports
│   │   ├── 7_1_provider_utilization.sql
│   │   ├── 7_2_inpatient_los_by_provider.sql
│   │   ├── 7_3_top_patients_by_cost.sql
│   │   ├── 7_4_procedure_volume_costs.sql
│   │   ├── 7_5_post_procedure_followup_14d.sql       # uses CTE + correlated EXISTS
│   │   └── 7_6_er_frequenters.sql
│   ├── sql_skill_demos/                               # Section 8: 9 required SQL skill demonstrations
│   │   ├── 2_inner_join_diagnosis_patient_condition.sql
│   │   ├── 3_left_outer_join_encounter_activity.sql
│   │   ├── 4_single_row_subquery.sql
│   │   ├── 5_multi_row_subquery_highrisk_er.sql      # uses CTE
│   │   ├── 6_aggregation.sql
│   │   ├── 7_not_in_subquery.sql
│   │   ├── 8_case_statement.sql
│   │   ├── 9_not_exists_inactive_providers.sql
│   │   └── 10_not_null_subquery.sql
│   └── archived_partial_dump_3of14.sql                # Historical mysqldump (3 of 14 rpt_ tables); kept for reference
└── reports/
    ├── INFO579-Final-Project-Report-Thompson.pdf      # Complete analysis (8.1MB)
    └── methodology_section.pdf                        # Methodology excerpt
```

---

## How to Reproduce

### With Docker

Prerequisites: Docker Desktop or OrbStack, Python 3.9+.

```bash
./setup.sh
```

Runtime ~30s. Populates `Final_Project` on `127.0.0.1:13306`.

Port 13306 was chosen over 3306 to avoid collision with a local MySQL install. Port 33060 was avoided because OrbStack auto-wraps it as MySQL X Protocol, which breaks standard clients.

```bash
# connect
docker compose exec mysql mysql -u root -pportfolio_demo_pw Final_Project

# stop (data persists)
docker compose down

# reset (deletes volume)
docker compose down -v
```

### Without Docker

Requires MySQL 8+ running locally and Python 3.9+.

```bash
pip install -r requirements.txt

mysql -u root -p -e "CREATE DATABASE Final_Project;"
mysql -u root -p Final_Project < sql/00_schema.sql

python scripts/load_csvs.py --user root --database Final_Project

for f in sql/analytical_reports/*.sql; do
  mysql -u root -p Final_Project < "$f"
done

# optional skill demos
for f in sql/sql_skill_demos/*.sql; do
  mysql -u root -p Final_Project < "$f"
done
```

### Loader behavior

Column-name mapping between Synthea CSVs and the schema, ISO-8601 datetime conversion (`2010-01-23T17:45:28Z` → `2010-01-23 17:45:28`), NULL handling for empty cells, foreign-key load ordering, batch inserts (1000 rows per call), idempotent re-runs (TRUNCATEs each table first). Analytical queries are idempotent (`DROP TABLE IF EXISTS` before `CREATE TABLE AS`).

Password: `$MYSQL_PASSWORD` env var, or interactive prompt if unset.

Each `.sql` file begins with a header comment describing the query.

### Row counts

The 8 base tables hold 446,783 rows:

| Table | Rows |
|---|---:|
| patient | 1,171 |
| provider | 5,855 |
| encounter | 53,346 |
| medical_condition | 8,376 |
| procedures | 34,981 |
| observation | 299,697 |
| diagnosis | 8,376 |
| treatment | 34,981 |

---

## Sample analytical findings

These charts come from running the queries against the populated database. Regenerate them anytime with `MYSQL_PASSWORD=portfolio_demo_pw python scripts/generate_charts.py --host 127.0.0.1 --port 13306 --user root --database Final_Project`.

### Top conditions by patient count

![Top 10 conditions](./images/top_conditions.png)

Viral upper-respiratory infections lead, followed by cardiometabolic findings (BMI 30+, prediabetes, hypertension). Pregnancy-related conditions appear in the bottom half.

### Top procedures by volume

![Top 10 procedures](./images/top_procedures.png)

Medication Reconciliation leads at 5,632 occurrences. The top procedures are non-surgical interventions: medication management, renal dialysis, obstetric monitoring, immunotherapy, intramuscular injection.

### Top providers by encounter count

![Top 10 providers](./images/top_providers.png)

One General Practice provider (Gaynell126 Streich926) handles 3,217 encounters, over 60% more than the second-busiest. All top 10 are General Practice, suggesting workload imbalance toward GPs vs. specialists.

### Patient coverage distribution

![Coverage distribution](./images/coverage_distribution.png)

Of 1,171 patients: 326 are high-coverage (≥$10K), 309 medium ($5K–$10K), 536 low (<$5K). Roughly 46% of patients have low healthcare coverage.

## Analytical Reports (9 documented + 5 schema-defined)

1. Provider Utilization
2. Inpatient LOS by Provider
3. Top Patients by Cost
4. Procedure Volume & Costs
5. 14-Day Follow-up Rates
6. ER Frequent Users
7. Diagnosis-Patient-Condition Mapping
8. Encounter Activity Tracking
9. High-Risk ER Patients by Provider
10. Inactive Providers by Specialty
11. Coverage Categories
12. Deceased Patient Encounters
13. Patients without Diagnoses
14. 30-Day Mortality Rates

**Queries by section:**
- [Section 7: 6 Analytical Reports](./sql/analytical_reports/)
- [Section 8: 9 SQL Skill Demonstrations](./sql/sql_skill_demos/)
- [Schema definition (8 base + 14 rpt tables + 12 FKs)](./sql/00_schema.sql)

> **A note on documented coverage:** The schema declares 14 `rpt_` tables; the final report PDF documents the SQL queries for **9 of them** (sections 7.1–7.6 + four `CREATE TABLE` statements in section 8). The remaining 5 (`rpt_condition_prevalence`, `rpt_inner_encounter_provider`, `rpt_proc_readmit_30d`, `rpt_provider_readmit_30d`, `rpt_readmissions_30d`) appear in the schema but their queries were not included in the final report; they're declared for completeness but not reproducible from this repo alone. The numbered list above counts both: 9 documented + 5 schema-only.

---

## Challenges Solved

### Bulk loading vs row-by-row inserts

For loading the data, I started by inserting rows one at a time. Then I found I could import the CSV files directly with LOAD DATA INFILE, which let me bulk insert every row at once. It went well after a few tweaks. The provider data also had some duplicate organization_id values, so I made a unique key on the paired provider_id and organization_id. That way I could still use both of them as foreign keys.

### Dirty foreign-key data (10.13% orphan rows)

For the observation data, I loaded it into a staging table first, then used INSERT and SELECT to move it into the real observation table while doing a LEFT JOIN on encounter_id. Any mismatched encounter_id would come in as NULL instead of breaking the load. I did a bit of investigation, and around 10.13% of the encounter_id values in the observation CSV were not found in the encounter table. I decided to keep these as NULL for future insights later if interested.

### Misleading mortality metric

One result I went back and corrected was the death rate by encounter class. At first it showed the top three as ambulatory, wellness, and outpatient. But those are typically scheduled visits, so a raw count there didn't really make sense as a measure of risk. I re-checked it using death within 30 days of a visit, as a rate per 1,000 encounters. That showed emergency and inpatient at the top instead, which made more sense.

---

## Academic Information

**Course**: INFO 579 - SQL & NoSQL Databases  
**Term**: 2024-2025  
**Institution**: University of Arizona

---

<p align="center">
  <em>University of Arizona, Data Science Portfolio</em>
</p>
