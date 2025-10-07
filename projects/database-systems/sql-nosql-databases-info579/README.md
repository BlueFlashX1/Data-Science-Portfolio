# SQL & NoSQL Databases - Healthcare Data Analysis

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 579](https://img.shields.io/badge/INFO%20579-SQL%20%26%20NoSQL%20Databases-red?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

[![SQL](https://img.shields.io/badge/SQL-Advanced%20Queries-4479A1?style=flat-square&logo=postgresql)](https://postgresql.org)
[![Python](https://img.shields.io/badge/Python-Data%20Analysis-3776AB?style=flat-square&logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square&logo=pandas)](https://pandas.pydata.org)
[![Healthcare](https://img.shields.io/badge/Domain-Healthcare%20Data-green?style=flat-square)](https://github.com)

> **COURSE FINAL PROJECT**: Advanced healthcare database analysis using SQL and NoSQL technologies with large-scale data processing

**Academic Context**: This is a final project for INFO 579 (SQL & NoSQL Databases) demonstrating advanced database querying, data analysis, and relationship modeling skills applied to complex healthcare datasets.

## Project Overview

This project demonstrates advanced database querying and schema design skills through analysis of patient relationships with multiple variables. The work showcases proficiency in handling complex many-to-many relationships and analytical query development.

### Research Focus
- **Patient Relationship Analysis**: Analysis of patient relationships across multiple healthcare variables
- **Healthcare Data Processing**: Structured synthetic healthcare data (Synthea^1)
- **Complex Relationship Patterns**: Many-to-many relationship modeling in healthcare systems  
- **NoSQL Integration**: Document-based data handling and analysis approaches

^1 *Synthea: Synthetic Patient Population Simulator - https://synthetichealth.github.io/synthea/*

## Dataset Overview
The project utilizes structured synthetic healthcare datasets with the following entities:

### Healthcare Dataset Files

| Dataset | File | Size | Records | Description | Download |
|---------|------|------|---------|-------------|----------|
| **Patients** | [`patients.csv`](./data/patients.csv) | 325KB | 1,171 | Demographics, addresses, financial info | 📁 [Download](./data/patients.csv) |
| **Encounters** | [`encounters.csv`](./data/encounters.csv) | 16MB | 53,346 | Medical visits, appointments, billing | 📁 [Download](./data/encounters.csv) |
| **Conditions** | [`conditions.csv`](./data/conditions.csv) | 1MB | 8,376 | Medical diagnoses and ICD-10 codes | 📁 [Download](./data/conditions.csv) |
| **Procedures** | [`procedures.csv`](./data/procedures.csv) | 5.4MB | ~25,000 | Medical procedures and CPT codes | 📁 [Download](./data/procedures.csv) |
| **Observations** | [`observations.csv`](./data/observations.csv) | 41MB | ~180,000 | Lab results, vital signs, measurements | 📁 [Download](./data/observations.csv) |
| **Providers** | [`providers.csv`](./data/providers.csv) | 1MB | 5,855 | Healthcare facilities and practitioners | 📁 [Download](./data/providers.csv) |

### Sample Data (Preview Files)

| Sample File | Size | Description | Access |
|-------------|------|-------------|--------|
| [`patients_sample.csv`](./data/patients_sample.csv) | 5KB | First 100 patient records | 🗋 [Preview](./data/patients_sample.csv) |
| [`conditions_sample.csv`](./data/conditions_sample.csv) | 6KB | Sample condition diagnoses | 🗋 [Preview](./data/conditions_sample.csv) |

### Data Relationships & Complexity
- **Primary Keys**: UUID-based patient, encounter, provider identifiers
- **Many-to-Many**: Patients ↔ Conditions, Patients ↔ Procedures, Providers ↔ Patients
- **Time Series**: Longitudinal encounters, observations with timestamps
- **Hierarchical**: Organizations → Providers → Encounters → Patients
- **Clinical Codes**: ICD-10 diagnoses, CPT procedure codes, LOINC observation codes
**Time Dimension**: Longitudinal patient records across multiple encounters

## Advanced SQL Analysis

### Comprehensive SQL Skills Demonstrated

Based on the 13+ analytical report tables created in this project, the following advanced SQL techniques were employed:

#### **1. Complex Multi-Table Joins & Relationship Analysis**
```sql
-- Example: 30-Day Readmission Analysis (rpt_readmissions_30d)
-- Demonstrates temporal joins with self-referencing encounter tables
SELECT 
    current.patient_id,
    current.encounter_id,
    current.encounter_start_date,
    prev.encounter_start_date as prev_start,
    DATEDIFF(current.encounter_start_date, prev.encounter_start_date) as days_since_prior
FROM encounter current
JOIN encounter prev ON current.patient_id = prev.patient_id
WHERE DATEDIFF(current.encounter_start_date, prev.encounter_start_date) BETWEEN 1 AND 30;
```

#### **2. Advanced Aggregation & Statistical Analysis**
```sql
-- Example: Condition Prevalence Analysis (rpt_condition_prevalence)
-- Demonstrates GROUP BY with statistical calculations
SELECT 
    condition_code,
    condition_description,
    COUNT(DISTINCT patient_id) as n_patients,
    ROUND((COUNT(DISTINCT patient_id) * 100.0 / (SELECT COUNT(*) FROM patient)), 2) as prevalence_rate
FROM diagnosis d
JOIN condition_codes c ON d.code = c.code
GROUP BY condition_code, condition_description
ORDER BY n_patients DESC;
```

#### **3. Window Functions & Analytical Queries**
```sql
-- Example: Provider Utilization Analysis (rpt_provider_utilization)
-- Demonstrates ROW_NUMBER, RANK, and aggregate window functions
SELECT 
    provider_id,
    provider_name,
    provider_specialty,
    COUNT(encounter_id) as n_encounters,
    ROW_NUMBER() OVER (PARTITION BY provider_specialty ORDER BY COUNT(encounter_id) DESC) as specialty_rank,
    AVG(COUNT(encounter_id)) OVER (PARTITION BY provider_specialty) as avg_specialty_encounters
FROM encounter e
JOIN provider p ON e.provider_id = p.provider_id
GROUP BY provider_id, provider_name, provider_specialty;
```

#### **4. Temporal Data Analysis & Date Functions**
```sql
-- Example: Encounter Activity Analysis (rpt_encounter_activity)
-- Demonstrates advanced date manipulation and time-series analysis
SELECT 
    DATE_FORMAT(encounter_date, '%Y-%m') as encounter_month,
    COUNT(*) as monthly_encounters,
    COUNT(DISTINCT patient_id) as unique_patients,
    LAG(COUNT(*), 1) OVER (ORDER BY DATE_FORMAT(encounter_date, '%Y-%m')) as prev_month_encounters,
    CASE 
        WHEN LAG(COUNT(*), 1) OVER (ORDER BY DATE_FORMAT(encounter_date, '%Y-%m')) IS NOT NULL 
        THEN ROUND(((COUNT(*) - LAG(COUNT(*), 1) OVER (ORDER BY DATE_FORMAT(encounter_date, '%Y-%m'))) * 100.0 / 
                    LAG(COUNT(*), 1) OVER (ORDER BY DATE_FORMAT(encounter_date, '%Y-%m'))), 2)
        ELSE NULL 
    END as month_over_month_growth
FROM encounter
GROUP BY DATE_FORMAT(encounter_date, '%Y-%m')
ORDER BY encounter_month;
```

#### **5. Subqueries & Nested Analytics**
```sql
-- Example: High-Risk ER Patients (rpt_providers_highrisk_er)
-- Demonstrates correlated subqueries and EXISTS clauses
SELECT DISTINCT
    p.patient_id,
    p.first_name,
    p.last_name,
    (
        SELECT COUNT(*) 
        FROM encounter e 
        WHERE e.patient_id = p.patient_id 
        AND e.encounter_class = 'emergency'
        AND e.encounter_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
    ) as er_visits_6months
FROM patient p
WHERE EXISTS (
    SELECT 1 FROM encounter e 
    WHERE e.patient_id = p.patient_id 
    AND e.encounter_class = 'emergency'
    GROUP BY e.patient_id 
    HAVING COUNT(*) > 5
);
```

#### **6. Advanced Healthcare Analytics Patterns**

**Clinical Quality Indicators:**
- **30-day readmission rates** - Patient safety metrics
- **Provider utilization patterns** - Resource allocation analysis
- **Condition prevalence tracking** - Population health surveillance
- **Procedure cost analysis** - Healthcare economics

**Multi-Dimensional Analysis:**
- **Patient-Provider-Condition relationships** - Complex many-to-many joins
- **Time-series healthcare trends** - Longitudinal data analysis
- **Risk stratification models** - Advanced patient categorization
- **Care pathway optimization** - Sequential encounter analysis

### SQL Techniques Mastery Level

| Technique Category | Skills Demonstrated | Complexity Level |
|-------------------|--------------------|-----------------|
| **Joins & Relationships** | Multi-table joins, self-joins, temporal joins | 🔴 Advanced |
| **Aggregation & Grouping** | Complex GROUP BY, HAVING, statistical functions | 🔴 Advanced |
| **Window Functions** | ROW_NUMBER, RANK, LAG/LEAD, analytical functions | 🔴 Advanced |
| **Temporal Analysis** | Date arithmetic, time-series patterns, intervals | 🔴 Advanced |
| **Subqueries** | Correlated subqueries, EXISTS, nested analytics | 🔴 Advanced |
| **Healthcare Domain** | Clinical coding, quality metrics, population health | 🔴 Expert |

**Total Analytical Reports Created**: 13+ comprehensive healthcare intelligence tables
**Query Complexity**: Enterprise-level healthcare analytics suitable for clinical decision support

## Project Files

### Core Documentation
| File | Size | Description |
|------|------|-------------|
| [`INFO579_Final Project_Report_Thompson.pdf`](./INFO579_Final%20Project_Report_Thompson.pdf) | 8.1MB | **Complete project analysis with findings and methodology** |

### Data Architecture
**Note**: Original healthcare datasets are referenced in the complete project report but not included in this portfolio version to maintain repository efficiency while preserving full analytical context.

## Healthcare Data Insights

### Clinical Relationship Patterns
The analysis reveals significant patterns in healthcare data relationships:

**Multi-condition Patients**:
- Identification of patients with complex medical histories
- Analysis of comorbidity patterns and disease correlations
- Healthcare resource utilization patterns

**Procedure-Patient Relationships**:
- Treatment pathway analysis for common conditions
- Resource allocation patterns across different patient populations
- Quality metrics for care delivery and patient outcomes

### Data Quality Findings
- **Referential Integrity**: Comprehensive validation of patient-condition linkages
- **Data Completeness**: Analysis of missing data patterns across healthcare entities
- **Temporal Consistency**: Verification of encounter sequences and care continuity


## Project Structure

```
sql-nosql-databases-info579/
├── README.md                                          # This documentation
├── INFO579_Final Project_Report_Thompson.pdf          # Complete project analysis
├── data/                                              # Healthcare dataset files
└── database-backup/                                   # SQL database backup files
```

## Technical Achievements

### Advanced SQL Techniques
- **Complex Multi-table Joins**: Efficient querying across 6+ healthcare entities
- **Temporal Analysis**: Time-series queries for longitudinal patient tracking
- **Aggregate Functions**: Advanced grouping and statistical analysis queries
- **Subquery Optimization**: Nested queries for complex healthcare analytics

### Data Analysis Innovation
- **Relationship Validation**: Automated verification of data integrity across entities
- **Pattern Recognition**: Identification of significant healthcare utilization patterns
- **Quality Metrics**: Comprehensive data quality assessment and reporting
- **Performance Optimization**: Efficient processing of large healthcare datasets

### Healthcare Domain Application
- **Clinical Workflow Understanding**: Database design supporting real healthcare operations
- **Privacy Considerations**: Awareness of HIPAA and healthcare data protection requirements
- **Interoperability**: Database structures supporting healthcare data exchange standards
- **Population Health**: Analysis supporting public health and epidemiological research

## Academic Information

**Course**: INFO 579 - SQL & NoSQL Databases  
**Institution**: University of Arizona  
**Project Type**: Final Course Project  
**Domain Focus**: Healthcare Data Management and Analysis  
**Data Scale**: Large-scale (67MB) healthcare dataset analysis  

### Learning Objectives Demonstrated
- **Advanced SQL Proficiency**: Complex query development for healthcare analytics
- **NoSQL Integration**: Document-based data handling and analysis approaches  
- **Data Integrity Management**: Automated validation and quality assurance processes
- **Healthcare Informatics**: Specialized knowledge in medical data standards and relationships
- **Python-SQL Integration**: Seamless integration of database queries with analytical processing
- **Large-Scale Data Handling**: Efficient processing of substantial healthcare datasets

## Healthcare Analytics Applications

### Clinical Decision Support
- **Patient Risk Assessment**: Multi-condition analysis for care planning
- **Resource Allocation**: Procedure utilization analysis for capacity planning
- **Quality Improvement**: Pattern identification for care optimization

### Population Health Management
- **Epidemiological Analysis**: Disease pattern recognition across patient populations  
- **Healthcare Utilization**: Service usage patterns and trend analysis
- **Outcome Prediction**: Data foundations for predictive healthcare modeling

### Research Applications
- **Clinical Research**: Database foundations for medical research studies
- **Health Services Research**: Healthcare delivery pattern analysis
- **Quality Metrics**: Evidence-based quality improvement initiatives

## File Recommendations

**For Complete Project Review**: Use [`INFO579_Final Project_Report_Thompson.pdf`](./INFO579_Final%20Project_Report_Thompson.pdf) - contains comprehensive analysis, methodology, findings, and healthcare insights with full technical documentation.

**For Database Access**: Explore [`database-backup/`](./database-backup/) - contains SQL database dumps and comprehensive documentation for database restoration and analysis.

## Future Enhancements

- **Real-time Analytics**: Streaming healthcare data processing for live clinical dashboards
- **Machine Learning Integration**: Predictive modeling for patient outcome forecasting  
- **NoSQL Expansion**: Document-based storage for unstructured clinical notes and imaging data
- **FHIR Integration**: Standards-compliant healthcare data exchange implementation
- **Security Enhancement**: HIPAA-compliant security measures and comprehensive audit trails

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.

---

<div align="center">

**Advanced healthcare data analysis demonstrating SQL and NoSQL database expertise**

*Bridging database technology with real-world healthcare data challenges*

</div>