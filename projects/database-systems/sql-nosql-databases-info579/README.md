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

| Entity | Description | Key Relationships |
|--------|-------------|------------------|
| **Patients** | Patient demographic and identity information | Core entity linking all clinical data |
| **Encounters** | Medical visits and appointments | Patient ↔ Provider interactions |
| **Conditions** | Medical diagnoses and conditions | Patient ↔ Diagnosis (many-to-many) |
| **Procedures** | Medical procedures and treatments | Patient ↔ Treatment (many-to-many) |
| **Observations** | Clinical measurements and test results | Patient ↔ Clinical data (time-series) |
| **Providers** | Healthcare providers and facilities | Provider ↔ Patient relationships |

**Relationship Complexity**: Multiple overlapping many-to-many relationships  
**Time Dimension**: Longitudinal patient records across multiple encounters

## Advanced SQL Analysis
- **Complex Relationship Queries**: Multi-table joins across healthcare entities
- **Temporal Data Analysis**: Time-series queries for patient progression tracking
- **Aggregate Analytics**: Patient outcome patterns and healthcare utilization metrics

## Project Files

### Core Documentation
| File | Size | Description |
|------|------|-------------|
| [`INFO579_Final Project_Report_Thompson.pdf`](./INFO579_Final%20Project_Report_Thompson.pdf) | 8.1MB | **Complete project analysis with findings and methodology** |
| [`INFO579_Final Project_Update2_Thompson.pdf`](./INFO579_Final%20Project_Update2_Thompson.pdf) | 709KB | Project development progress and interim analysis |

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
└── INFO579_Final Project_Update2_Thompson.pdf         # Project development progress
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

**For Development Process**: Examine [`INFO579_Final Project_Update2_Thompson.pdf`](./INFO579_Final%20Project_Update2_Thompson.pdf) - shows project evolution, interim findings, and analytical development process.

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