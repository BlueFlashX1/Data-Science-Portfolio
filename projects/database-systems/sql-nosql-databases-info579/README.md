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

## SQL Query Examples

The project demonstrates proficiency with advanced SQL concepts:

- **INNER JOIN**: Three-table join (diagnosis → patient → medical_condition) for disease prevalence
- **LEFT OUTER JOIN**: Encounter-provider-procedure joins to identify missing provider assignments
- **Single-row Subquery**: `SELECT MAX(healthcare_expenses)` to find highest-cost patient
- **Multiple-row Subquery**: High-risk ER patients (`IN` clause) matched with provider specialties
- **Aggregation**: Multi-column GROUP BY for provider specialty procedure volumes
- **NOT IN Operator**: Patients without recorded diagnoses
- **CASE Statements**: Healthcare coverage categorization (high/medium/low tiers)
- **NOT EXISTS**: Inactive providers with zero encounters by specialty
- **NOT NULL**: Encounter classes for deceased patients

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
