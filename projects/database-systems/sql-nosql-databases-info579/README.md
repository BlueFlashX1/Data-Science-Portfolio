# Healthcare Analytics with SQL & NoSQL

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](./INFO579_Final%20Project_Report_Thompson.pdf)
[![INFO 579](https://img.shields.io/badge/INFO%20579-SQL%20%26%20NoSQL-red?style=for-the-badge)](https://arizona.edu)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

> **Course project on database design and SQL analytics for healthcare data** — University of Arizona, INFO 579

**[View Full Report (PDF)](./INFO579_Final%20Project_Report_Thompson.pdf)** (8.1MB)

---

## Project Overview

I designed normalized database schemas and wrote complex SQL queries to analyze synthetic EHR data. I built 14 analytical reports addressing clinical quality, provider utilization, readmissions, and profitability.

**Key Metrics**: 1,171 patients • 53,346 encounters • 8,376 diagnoses • 67MB Synthea EHR data

---

## What I Applied

### SQL Techniques Implemented

| Category              | Techniques                                                  |
| --------------------- | ----------------------------------------------------------- |
| **Joins**             | Implemented multi-table joins (4+), LEFT/INNER variations, self-joins         |
| **Temporal Analysis** | Used `DATEDIFF`, `DATE_ADD` for 30-day readmission tracking      |
| **Advanced Queries**  | Built CTEs (Common Table Expressions) and correlated subqueries      |
| **Aggregation**       | Applied `GROUP BY` + `HAVING`, `CASE` for dynamic categorization    |
| **ETL**               | Executed `LOAD DATA INFILE` bulk import, Python-Pandas preprocessing |

### Database Design

- **3NF Normalization**: Designed 8 entity tables with 2 junction tables for many-to-many relationships
- **Foreign Keys**: Implemented 12 FK constraints with cascading relationships (patient→encounter→provider)
- **Schema Verified**: Verified record counts via AUTO_INCREMENT values in MySQL dump

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
├── README.md                                    # Project documentation
├── INFO579_Final Project_Report_Thompson.pdf    # Complete analysis (8.1MB)
├── data/                                        # 6 healthcare CSVs (67MB total)
│   ├── patients.csv
│   ├── encounters.csv
│   ├── conditions.csv
│   ├── procedures.csv
│   ├── observations.csv
│   └── providers.csv
└── database-backup/
    ├── Final_Project_schema.sql                 # Database structure (19KB)
    └── Final_Project_analytics_reports.sql      # 14 report tables with data (3.5MB)
```

---

## 14 Analytical Reports

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

**[View All SQL Queries](./database-backup/Final_Project_analytics_reports.sql)**

---

## Quick Start

### Prerequisites

- MySQL 8.0+
- Python 3.9+ with Pandas (for ETL)

### Database Setup

```bash
# Create database and load schema
mysql -u root -p < database-backup/Final_Project_schema.sql

# Load analytical reports (contains report data)
mysql -u root -p final_project < database-backup/Final_Project_analytics_reports.sql
```

### View Report

Open [`INFO579_Final Project_Report_Thompson.pdf`](./INFO579_Final%20Project_Report_Thompson.pdf) for complete analysis with visualizations.

---

<details>
<summary><strong>Sample SQL Implementations</strong> (Click to expand)</summary>

### 30-Day Readmission Tracking

```sql
CREATE TABLE rpt_readmissions_30d AS
SELECT
  e1.patient_id,
  e1.encounter_id AS first_encounter,
  e2.encounter_id AS readmit_encounter,
  DATEDIFF(e2.encounter_start_date, e1.encounter_end_date) AS days_since_prior
FROM encounter e1
JOIN encounter e2
  ON e1.patient_id = e2.patient_id
  AND e2.encounter_start_date > e1.encounter_end_date
  AND e2.encounter_start_date <= DATE_ADD(e1.encounter_end_date, INTERVAL 30 DAY);
```

### Coverage Tier Analysis

```sql
SELECT
  SUM(CASE WHEN healthcare_coverage >= 10000 THEN 1 ELSE 0 END) AS high_coverage,
  SUM(CASE WHEN healthcare_coverage BETWEEN 5000 AND 9999 THEN 1 ELSE 0 END) AS medium_coverage,
  SUM(CASE WHEN healthcare_coverage < 5000 THEN 1 ELSE 0 END) AS low_coverage
FROM patient;
```

</details>

---

## Academic Information

**Course**: INFO 579 - SQL & NoSQL Databases  
**Term**: 2024-2025  
**Institution**: University of Arizona

---

<p align="center">
  <em>University of Arizona — Graduate Student Data Science Portfolio</em>
</p>
