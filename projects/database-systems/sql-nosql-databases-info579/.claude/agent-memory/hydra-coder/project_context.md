---
name: project-context
description: INFO579 SQL/NoSQL portfolio project — schema, data sources, and loader script
metadata:
  type: project
---

Healthcare database portfolio project for INFO579 Final Project.

**Why:** Recruiter-facing reproducibility — anyone cloning the repo can populate MySQL from Synthea CSVs with one command.

**Stack:** MySQL 8, Python 3.9+, pandas, mysql-connector-python

**Key files:**
- `sql/00_schema.sql` — creates Final_Project database (8 base tables + ~14 rpt_ tables)
- `data/*.csv` — 6 Synthea CSVs (patients, providers, encounters, conditions, procedures, observations)
- `scripts/load_csvs.py` — CSV loader (written 2026-05-24)
- `requirements.txt` — pandas>=2.0.0, mysql-connector-python>=8.3.0
- `sql/analytical_reports/*.sql` — 6 report-materialization queries run AFTER base load

**Loading order (FK dependency chain):**
1. patient (patients.csv)
2. provider (providers.csv)
3. encounter (encounters.csv) — FK to patient, provider
4. medical_condition (conditions.csv) — FK to patient, encounter; AUTO_INCREMENT condition_id
5. procedures (procedures.csv) — FK to patient, encounter; AUTO_INCREMENT procedure_id
6. observation (observations.csv) — FK to patient, encounter; AUTO_INCREMENT observation_id
7. diagnosis — derived: INSERT INTO diagnosis SELECT DISTINCT patient_id, condition_id FROM medical_condition
8. treatment — derived: INSERT INTO treatment SELECT DISTINCT patient_id, procedure_id FROM procedures

**How to apply:** If revisiting this project, the loader script is complete. Next steps would be running 00_schema.sql first, then load_csvs.py, then the analytical_reports/ SQLs.
