# Healthcare Analytics with SQL & NoSQL

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 579](https://img.shields.io/badge/INFO%20579-SQL%20%26%20NoSQL%20Databases-red?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

> **Advanced database design and querying for healthcare analytics** • University of Arizona, INFO 579 Final Project

Database system implementing normalized schemas, complex SQL queries, and temporal analysis on synthetic EHR data. Built 14 analytical reports for clinical quality indicators, readmission tracking, and population health surveillance.

**Key Finding**: 90% 30-day readmission rate • 63% viral sinusitis prevalence • 1,171 patients • 53K+ encounters

**Tech Stack**: MySQL • Complex SQL Joins • Temporal Analysis • Python • Pandas • Healthcare Domain Analytics

**[View Full Report](./INFO579_Final%20Project_Report_Thompson.pdf)** (8.1MB PDF)

---

## Project Structure

```
sql-nosql-databases-info579/
├── README.md                                    # Project documentation
├── INFO579_Final Project_Report_Thompson.pdf    # Complete analysis report
├── data/                                        # 6 healthcare CSV datasets (67MB total)
└── database-backup/                             # SQL schemas and sample data
    ├── Final_Project_schema.sql                # Database structure
    ├── Final_Project_sample_data.sql           # Sample records
    └── Final_Project_analytics_reports.sql      # 14 analytical queries
```

## Healthcare Dataset

**6 Entities • 67MB Total • Synthea Synthetic EHR Data**

| Entity           | File                                          | Size  | Records  | Description                             |
| ---------------- | --------------------------------------------- | ----- | -------- | --------------------------------------- |
| **Patients**     | [`patients.csv`](./data/patients.csv)         | 325KB | 1,171    | Demographics, addresses, financial info |
| **Encounters**   | [`encounters.csv`](./data/encounters.csv)     | 16MB  | 53,346   | Medical visits, appointments, billing   |
| **Conditions**   | [`conditions.csv`](./data/conditions.csv)     | 1MB   | 8,376    | Medical diagnoses with ICD-10 codes     |
| **Procedures**   | [`procedures.csv`](./data/procedures.csv)     | 5.4MB | ~25,000  | Medical procedures with CPT codes       |
| **Observations** | [`observations.csv`](./data/observations.csv) | 41MB  | ~180,000 | Lab results, vital signs, measurements  |
| **Providers**    | [`providers.csv`](./data/providers.csv)       | 1MB   | 5,855    | Healthcare facilities and practitioners |

---

## Business Objectives

This project addresses five core healthcare analytics objectives:

1. **Increase Profitability** - Track procedure costs and identify high-cost patients for intervention strategies
2. **Improve Clinical Quality** - Monitor follow-up rates, length of stay (LOS), and condition management effectiveness
3. **Optimize Provider Utilization** - Balance workloads and identify capacity underutilization across specialties
4. **Reduce Readmissions** - Flag high-risk patients with frequent ER visits for streamlined care
5. **Strategic Expansion** - Identify high-demand services and resource allocation opportunities

---

## SQL Techniques & Implementation

### Database Design

- **Normalized Schemas**: Third normal form (3NF) across 6 healthcare entities
- **Referential Integrity**: Foreign key constraints (`patient→encounter→provider→diagnosis`)
- **Junction Tables**: Resolved many-to-many relationships (patient-conditions, patient-procedures)
- **Unique Keys**: Combined `provider_id + organization_id` for entity relationship integrity
- **Strategic Indexing**: Primary and foreign key indexes for optimized join performance

### Advanced SQL Techniques

- **Complex Multi-table Joins**: 4+ table joins with LEFT/INNER JOIN variations
- **Temporal Analysis**: `DATEDIFF` operations for 30-day readmission tracking
- **Window Functions**: Patient visit sequencing and encounter history analysis
- **Advanced Aggregation**: `GROUP BY` with `HAVING` clauses for disease prevalence
- **Subqueries**: Single-row (`MAX`), multiple-row (`IN`), and correlated (`NOT EXISTS`)
- **CASE Statements**: Dynamic categorization (e.g., coverage tiers: high/medium/low)
- **Common Table Expressions (CTEs)**: Simplified complex query logic for readability

### 14 Analytical Reports Created

1. **Provider Utilization** - Encounters per provider and specialty
2. **Inpatient LOS by Provider** - Average length of stay analysis
3. **Top Patients by Cost** - High-expenditure patient identification
4. **Procedure Volume & Costs** - Most common procedures and average costs
5. **14-Day Follow-up Rates** - Post-procedure care quality metrics
6. **ER Frequent Users** - High-risk patients (≥3 ER visits)
7. **Diagnosis-Patient-Condition** - Disease prevalence by patient count
8. **Encounter Activity** - Provider assignment validation
9. **Providers with High-Risk ER Patients** - Specialty-level risk distribution
10. **Inactive Providers by Specialty** - Zero-encounter provider tracking
11. **Coverage Categories** - Patient insurance tier distribution
12. **Deceased Patient Encounters** - Mortality by encounter class
13. **Patients without Diagnoses** - Data completeness validation
14. **30-Day Death Rates** - Mortality rates per 1,000 encounters by class

### Data Integration & ETL

- **Bulk Loading**: `LOAD DATA INFILE` for efficient CSV import (67MB total)
- **Staging Tables**: Intermediate tables for data validation before final insert
- **Python-Pandas Integration**: Data preprocessing and integrity checks
- **Null Handling**: 10.13% encounter mismatches identified and preserved for analysis
- **Data Quality**: Foreign key validation with LEFT JOIN to detect orphaned records

---

## Key Findings & Insights

### Clinical Quality

- **Top 5 Conditions**: Viral sinusitis (63% prevalence), acute viral pharyngitis, acute bronchitis, obesity (BMI 30+), prediabetes
- **Condition Patterns**: Upper-respiratory infections and cardiometabolic risk conditions most common
- **30-Day Mortality Rates**: Emergency (3.57 per 1,000) and inpatient (2.94 per 1,000) highest; ambulatory/wellness negligible
- **Follow-up Quality**: 14-day post-procedure follow-up rates tracked across all procedure types

### Cost & Resource Utilization

- **High-Volume Procedures**: Medication reconciliation, renal dialysis, fetal heart auscultation, immunotherapy (1,000+ occurrences each)
- **Procedure Costs**: Non-surgical interventions dominate; most expensive procedures exceed $10,000
- **Provider Workload Imbalance**: Top provider (Gaynell126 Streich926) handled 3,000+ encounters; rapid drop-off indicates uneven allocation
- **High-Cost Patients**: Identified for targeted financial assistance and care coordination strategies

### Provider Performance

- **Inactive Specialties**: Internal medicine, nurse practitioners, clinical social workers, physician assistants, physical therapy (zero encounters)
- **Specialty Focus**: General practice providers handle majority of encounters
- **Inpatient LOS**: Tracked per provider to identify efficiency outliers requiring intervention

### Population Health Surveillance

- **ER Frequent Users**: Patients with ≥3 emergency visits flagged for streamlined check-ins
- **Data Completeness**: 19 patients without recorded diagnoses; 10.13% observation encounters without matching encounter records
- **Coverage Distribution**: 536 low coverage (<$5K), 309 medium ($5K-$10K), 326 high (≥$10K)
- **53,346 encounters** analyzed across **1,171 unique patients**

---

## SQL Code Samples

### Complex Join with Temporal Analysis (30-Day Readmission Tracking)

```sql
CREATE TABLE rpt_readmissions_30d AS
SELECT 
  e1.patient_id,
  e1.encounter_id AS first_encounter,
  e2.encounter_id AS readmit_encounter,
  e1.encounter_start_date AS prev_start,
  e2.encounter_start_date AS readmit_start,
  DATEDIFF(e2.encounter_start_date, e1.encounter_end_date) AS days_since_prior
FROM encounter e1
JOIN encounter e2 
  ON e1.patient_id = e2.patient_id
  AND e2.encounter_start_date > e1.encounter_end_date
  AND e2.encounter_start_date <= DATE_ADD(e1.encounter_end_date, INTERVAL 30 DAY)
ORDER BY e1.patient_id, e1.encounter_start_date;
```

### CTE with Multiple-Row Subquery (High-Risk ER Patients by Provider)

```sql
CREATE TABLE rpt_providers_highrisk_er AS
WITH provider_tot AS (
  SELECT provider_id, organization_id, COUNT(*) AS total_encounters
  FROM encounter
  GROUP BY provider_id, organization_id
),
highrisk_patients AS (
  SELECT e.patient_id
  FROM encounter e
  WHERE LOWER(e.encounter_class) = 'emergency'
  GROUP BY e.patient_id
  HAVING COUNT(*) >= 10
)
SELECT 
  pr.provider_id,
  pr.provider_specialty,
  COUNT(DISTINCT e.patient_id) AS n_highrisk_patients,
  COUNT(*) AS n_highrisk_encounters,
  ROUND(100 * COUNT(*) / NULLIF(pt.total_encounters, 0), 2) AS pct_of_provider_encounters
FROM provider pr
JOIN encounter e 
  ON e.provider_id = pr.provider_id
JOIN provider_tot pt 
  ON pt.provider_id = pr.provider_id
WHERE e.patient_id IN (SELECT patient_id FROM highrisk_patients)
GROUP BY pr.provider_id, pr.provider_specialty, pt.total_encounters;
```

### CASE Statement with Aggregation (Coverage Tier Analysis)

```sql
SELECT
  SUM(CASE WHEN healthcare_coverage >= 10000 THEN 1 ELSE 0 END) AS high_coverage_count,
  SUM(CASE WHEN healthcare_coverage >= 5000 AND healthcare_coverage < 10000 
           THEN 1 ELSE 0 END) AS medium_coverage_count,
  SUM(CASE WHEN healthcare_coverage < 5000 THEN 1 ELSE 0 END) AS low_coverage_count
FROM patient;
```

### Window Functions with Aggregation (Post-Procedure Follow-up Rate)

```sql
CREATE TABLE rpt_followup_14d_by_proc_code AS
WITH proc_flags AS (
  SELECT 
    prc.procedure_code,
    prc.procedure_description,
    CASE
      WHEN EXISTS (
        SELECT 1
        FROM observation o
        WHERE o.patient_id = prc.patient_id
        AND o.observation_date > prc.procedure_date
        AND o.observation_date <= DATE_ADD(prc.procedure_date, INTERVAL 14 DAY)
      ) THEN 1 ELSE 0
    END AS has_followup_14d
  FROM procedures prc
)
SELECT 
  procedure_code,
  procedure_description,
  COUNT(*) AS n_procedures,
  SUM(has_followup_14d) AS n_with_followup_14d,
  ROUND(100 * SUM(has_followup_14d) / NULLIF(COUNT(*), 0), 2) AS pct_with_followup_14d
FROM proc_flags
GROUP BY procedure_code, procedure_description
ORDER BY pct_with_followup_14d ASC;
```

---

## Technologies

**Database**: MySQL • Normalized Schema Design (3NF) • Complex SQL Joins  
**SQL Techniques**: Subqueries • CTEs • Window Functions • Temporal Analysis • Aggregation  
**Integration**: Python • Pandas • Bulk CSV Loading • Data Validation  
**Domain**: Healthcare Analytics • EHR Data (Synthea) • Clinical Quality Indicators  
**Data Processing**: ETL Pipelines • Staging Tables • Foreign Key Validation

---

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.
