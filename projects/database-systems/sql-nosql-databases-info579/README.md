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
| Patients | [`patients.csv`](./data/patients.csv) | 325KB | 1,171 | Demographics, addresses, financial info | [Download](./data/patients.csv) |
| Encounters | [`encounters.csv`](./data/encounters.csv) | 16MB | 53,346 | Medical visits, appointments, billing | [Download](./data/encounters.csv) |
| Conditions | [`conditions.csv`](./data/conditions.csv) | 1MB | 8,376 | Medical diagnoses and ICD-10 codes | [Download](./data/conditions.csv) |
| Procedures | [`procedures.csv`](./data/procedures.csv) | 5.4MB | ~25,000 | Medical procedures and CPT codes | [Download](./data/procedures.csv) |
| Observations | [`observations.csv`](./data/observations.csv) | 41MB | ~180,000 | Lab results, vital signs, measurements | [Download](./data/observations.csv) |
| Providers | [`providers.csv`](./data/providers.csv) | 1MB | 5,855 | Healthcare facilities and practitioners | [Download](./data/providers.csv) |



## Advanced SQL Analysis

| Technique | Application |
|-----------|-------------|
| Complex Multi-table Joins | Patient, encounter, provider, and condition data integration |
| Temporal Analysis | 30-day readmission tracking and longitudinal healthcare trends |
| Window Functions | Provider utilization rankings and time-series analytics |
| Advanced Aggregation | Condition prevalence rates and statistical healthcare metrics |
| Subqueries & CTEs | High-risk patient identification and nested healthcare analytics |
| Healthcare Domain Analytics | Clinical quality indicators and population health surveillance |
| Data Validation | Automated referential integrity checks across healthcare entities |
| Performance Optimization | Efficient processing of large-scale healthcare datasets |

## Project Files

### Core Documentation
| File | Size | Description |
|------|------|-------------|
| [`INFO579_Final Project_Report_Thompson.pdf`](./INFO579_Final%20Project_Report_Thompson.pdf) | 8.1MB | **Complete project analysis with findings and methodology** |




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
- Complex Multi-table Joins: Efficient querying across 6+ healthcare entities
- Temporal Analysis: Time-series queries for longitudinal patient tracking
- Aggregate Functions: Advanced grouping and statistical analysis queries
- Subquery Optimization: Nested queries for complex healthcare analytics

### Data Analysis Innovation
- Relationship Validation: Automated verification of data integrity across entities
- Pattern Recognition: Identification of significant healthcare utilization patterns
- Quality Metrics: Comprehensive data quality assessment and reporting
- Performance Optimization: Efficient processing of large healthcare datasets

### Healthcare Domain Application
- Clinical Workflow Understanding: Database design supporting real healthcare operations
- Privacy Considerations: Awareness of HIPAA and healthcare data protection requirements
- Interoperability: Database structures supporting healthcare data exchange standards
- Population Health: Analysis supporting public health and epidemiological research

## Academic Information

Course: INFO 579 - SQL & NoSQL Databases  
Institution: University of Arizona  
Project Type: Final Course Project  
Domain Focus: Healthcare Data Management and Analysis  
Data Scale: Large-scale (67MB) healthcare dataset analysis

## Healthcare Analytics Applications

### Clinical Decision Support
- Patient Risk Assessment: Multi-condition analysis for care planning
- Resource Allocation: Procedure utilization analysis for capacity planning
- Quality Improvement: Pattern identification for care optimization

### Population Health Management
- Epidemiological Analysis: Disease pattern recognition across patient populations  
- Healthcare Utilization: Service usage patterns and trend analysis
- Outcome Prediction: Data foundations for predictive healthcare modeling

### Research Applications
- Clinical Research: Database foundations for medical research studies
- Health Services Research: Healthcare delivery pattern analysis
- Quality Metrics: Evidence-based quality improvement initiatives

## File Recommendations

For Complete Project Review: Use [`INFO579_Final Project_Report_Thompson.pdf`](./INFO579_Final%20Project_Report_Thompson.pdf) - contains comprehensive analysis, methodology, findings, and healthcare insights with full technical documentation.

For Database Access: Explore [`database-backup/`](./database-backup/) - contains SQL database dumps and comprehensive documentation for database restoration and analysis.

## Future Enhancements

- Real-time Analytics: Streaming healthcare data processing for live clinical dashboards
- Machine Learning Integration: Predictive modeling for patient outcome forecasting  
- NoSQL Expansion: Document-based storage for unstructured clinical notes and imaging data
- FHIR Integration: Standards-compliant healthcare data exchange implementation
- Security Enhancement: HIPAA-compliant security measures and comprehensive audit trails

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.

---

<div align="center">

**Advanced healthcare data analysis demonstrating SQL and NoSQL database expertise**

*Bridging database technology with real-world healthcare data challenges*

</div>