# Healthcare Analytics with SQL & NoSQL

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 579](https://img.shields.io/badge/INFO%20579-SQL%20%26%20NoSQL%20Databases-red?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

> **Advanced database design and querying for healthcare analytics** • University of Arizona, INFO 579 Final Project

Database system implementing normalized schemas, complex SQL queries, and temporal analysis on synthetic EHR data. Built 14 analytical reports for clinical quality indicators, readmission tracking, and population health surveillance.

**Key Metrics**: 1,171 patients • 53,346 encounters • 8,376 diagnoses • 67MB Synthea EHR data

**Hard Skills**: MySQL • Complex SQL Joins • CTEs • Window Functions • Temporal Analysis • 3NF Normalized Design • Python • Pandas

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

## Technical Implementation

### Technologies

**Database**: MySQL • 3NF Normalized Schemas • Foreign Key Constraints  
**SQL**: Complex Joins • CTEs • Window Functions • Temporal Analysis • Subqueries  
**ETL**: Python • Pandas • Bulk CSV Loading • Staging Tables  
**Domain**: Healthcare Analytics • Synthea EHR Data • Clinical Quality Metrics

### Database Architecture

**Normalized Design (3NF)** • 6 healthcare entities with referential integrity constraints  
**Foreign Keys**: `patient→encounter→provider→diagnosis` cascading relationships  
**Junction Tables**: Many-to-many resolution (patient-conditions, patient-procedures)  
**Strategic Indexing**: Primary/foreign key optimization for multi-table joins

### SQL Techniques Demonstrated

| Category              | Techniques                                                                    |
| --------------------- | ----------------------------------------------------------------------------- |
| **Joins**             | Multi-table (4+), LEFT/INNER variations, self-joins                           |
| **Temporal Analysis** | `DATEDIFF`, `DATE_ADD` for 30-day readmission tracking                        |
| **Advanced Queries**  | CTEs (Common Table Expressions), correlated subqueries (`EXISTS`, `NOT EXISTS`) |
| **Aggregation**       | `GROUP BY` + `HAVING`, `CASE` statements for dynamic categorization           |
| **Subqueries**        | Single-row (`MAX`), multiple-row (`IN`), scalar and derived tables            |
| **Data Validation**   | `LEFT JOIN` for orphaned records, null handling, foreign key integrity checks |
| **ETL**               | `LOAD DATA INFILE` bulk import, staging tables, Python-Pandas preprocessing   |

### 14 Analytical Reports

Provider Utilization • Inpatient LOS by Provider • Top Patients by Cost • Procedure Volume & Costs • 14-Day Follow-up Rates • ER Frequent Users • Diagnosis-Patient-Condition Mapping • Encounter Activity Tracking • High-Risk ER Patients by Provider • Inactive Providers by Specialty • Coverage Categories • Deceased Patient Encounters • Patients without Diagnoses • 30-Day Mortality Rates

**[View All SQL Queries](./database-backup/Final_Project_analytics_reports.sql)**

---

## Key Findings & Recommendations

Analysis organized by the five business objectives, with proposed strategies:

### 1. Increase Profitability

**Findings:**  
• High-Cost Patient Identification: Top patient expenses reached $1,108,789.93  
• High-Volume Procedures: Medication reconciliation, renal dialysis, fetal heart auscultation, uterine fundal height evaluation, subcutaneous immunotherapy, intramuscular injection (1,000+ occurrences each)  
• Procedure Cost Analysis: Non-surgical interventions dominate; procedures typically exceed $10,000  
• Coverage Distribution: 536 low (<$5K) • 309 medium ($5K-$10K) • 326 high (≥$10K)

**Proposed Strategy:** Implement targeted financial assistance programs for high-cost patients; streamline non-surgical intervention workflows to improve efficiency and reduce costs

### 2. Improve Clinical Quality

**Findings:**  
• Top 5 Conditions: Viral sinusitis (63% prevalence), acute viral pharyngitis, acute bronchitis, obesity (BMI 30+), prediabetes  
• Condition Patterns: Acute upper-respiratory infections and cardiometabolic risk conditions most common  
• 30-Day Mortality Rates: Emergency (3.57 per 1,000 encounters) • Inpatient (2.94 per 1,000) • Ambulatory/wellness/outpatient (negligible)  
• Post-Procedure Follow-up: 14-day follow-up rates tracked for quality of care assessment  
• Inpatient Length of Stay: Tracked per provider to identify efficiency outliers

**Proposed Strategy:** Develop preventive care programs for upper-respiratory infections and cardiometabolic conditions; improve inpatient efficiency for providers with extended LOS patterns; enhance post-procedure follow-up protocols

### 3. Optimize Provider Utilization

**Findings:**  
• Provider Workload Imbalance: Top provider (Gaynell126 Streich926) handled 3,000+ encounters; rapid drop-off to <2,000 encounters for other providers  
• Top 6 High-Volume Providers: Gaynell126 Streich926, Gertrudis163 Schaden604, Vern731 Powlowski563, Jeanmarie510 Beatty507, Maile198 Frami345, Luke971 Rath779 (all general practice)  
• Top 5 Inactive Specialties: Internal medicine, nurse practitioners, clinical social workers, physician assistants, physical therapy (zero encounters)  
• Specialty Analysis: Inactive specialties primarily function in ambulatory/outpatient settings

**Proposed Strategy:** Redistribute patient load across general practice providers to balance workloads; evaluate inactive specialties for budget reallocation or targeted activation based on demand

### 4. Reduce Readmissions

**Findings:**  
• 30-Day Readmission Tracking: Temporal analysis using `DATEDIFF` identifies patients readmitted within 30 days  
• ER High-Risk Patients: Patients with ≥3 emergency visits flagged for intervention  
• Post-Procedure Follow-up Quality: 14-day follow-up rates indicate service quality and readmission risk

**Proposed Strategy:** Implement streamlined check-in processes for high-risk ER patients to reduce wait times; enhance post-procedure follow-up care to prevent readmissions; develop proactive outreach for 30-day readmission patterns

### 5. Strategic Expansion

**Findings:**  
• High-Demand Service Lines: Non-surgical interventions (therapies, evaluations, medications) heavily utilized  
• Cost-Intensive Services: Procedures typically exceed $10,000, indicating need for efficiency investments  
• Common Condition Categories: Acute upper-respiratory infections, cardiometabolic risk, chronic conditions, obstetric events  
• Capacity Assessment: Inactive specialties and zero-procedure areas suggest reallocation opportunities  
• Dataset Scale: 53,346 encounters analyzed across 1,171 unique patients

**Proposed Strategy:** Invest in equipment and workflow improvements for high-cost non-surgical procedures to improve efficiency and reduce costs; expand services in high-demand areas (respiratory, cardiometabolic, obstetrics); maximize budgeting toward frequent specialties while selectively activating lacking specialties based on strategic need

---

<details>
<summary><strong>📝 Sample SQL Implementations</strong> (Click to expand)</summary>

### 30-Day Readmission Tracking (Temporal Analysis)

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

### High-Risk ER Patients by Provider (CTE + Subquery)

```sql
CREATE TABLE rpt_providers_highrisk_er AS
WITH provider_tot AS (
  SELECT provider_id, COUNT(*) AS total_encounters
  FROM encounter
  GROUP BY provider_id
),
highrisk_patients AS (
  SELECT patient_id
  FROM encounter
  WHERE LOWER(encounter_class) = 'emergency'
  GROUP BY patient_id
  HAVING COUNT(*) >= 10
)
SELECT
  pr.provider_id,
  pr.provider_specialty,
  COUNT(DISTINCT e.patient_id) AS n_highrisk_patients,
  ROUND(100 * COUNT(*) / NULLIF(pt.total_encounters, 0), 2) AS pct_encounters
FROM provider pr
JOIN encounter e ON e.provider_id = pr.provider_id
JOIN provider_tot pt ON pt.provider_id = pr.provider_id
WHERE e.patient_id IN (SELECT patient_id FROM highrisk_patients)
GROUP BY pr.provider_id, pr.provider_specialty, pt.total_encounters;
```

### Coverage Tier Analysis (CASE Aggregation)

```sql
SELECT
  SUM(CASE WHEN healthcare_coverage >= 10000 THEN 1 ELSE 0 END) AS high_coverage,
  SUM(CASE WHEN healthcare_coverage BETWEEN 5000 AND 9999 THEN 1 ELSE 0 END) AS medium_coverage,
  SUM(CASE WHEN healthcare_coverage < 5000 THEN 1 ELSE 0 END) AS low_coverage
FROM patient;
```

### Post-Procedure Follow-up Rate (Window Functions)

```sql
CREATE TABLE rpt_followup_14d_by_proc_code AS
WITH proc_flags AS (
  SELECT
    procedure_code,
    procedure_description,
    CASE WHEN EXISTS (
      SELECT 1 FROM observation o
      WHERE o.patient_id = prc.patient_id
      AND o.observation_date BETWEEN prc.procedure_date AND DATE_ADD(prc.procedure_date, INTERVAL 14 DAY)
    ) THEN 1 ELSE 0 END AS has_followup
  FROM procedures prc
)
SELECT
  procedure_code,
  COUNT(*) AS total_procedures,
  SUM(has_followup) AS with_followup,
  ROUND(100 * SUM(has_followup) / NULLIF(COUNT(*), 0), 2) AS followup_rate_pct
FROM proc_flags
GROUP BY procedure_code
ORDER BY followup_rate_pct ASC;
```

</details>

---

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.
