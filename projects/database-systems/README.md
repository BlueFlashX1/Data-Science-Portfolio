# Database Systems Projects

[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

> **Course project on database design and SQL analytics for healthcare data**

## Featured Project

### [Healthcare Analytics Database System](./sql-nosql-databases-info579/)

**INFO 579 - SQL & NoSQL Databases** | Final Project

![MySQL](https://img.shields.io/badge/MySQL_8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

**Project Scope**

- **67MB Synthea EHR Dataset**: 1,171 patients, 53,346 encounters across 6 entities
- **3NF Database Design**: Normalized schema with 12 foreign key constraints
- **14 Analytical Reports**: SQL queries for clinical quality and population health
- **Schema Verified**: Record counts confirmed via MySQL AUTO_INCREMENT values

**What I Applied**

| Objective                | Key Finding                                                            |
| ------------------------ | ---------------------------------------------------------------------- |
| **Clinical Quality**     | Identified viral sinusitis as most prevalent (63% of patients)         |
| **Provider Utilization** | Discovered severe workload imbalance (top provider: 3,000+ encounters) |
| **Readmissions**         | Flagged high-risk ER patients (≥3 visits) for intervention             |
| **30-Day Mortality**     | Calculated emergency mortality rate: 3.57 per 1,000 encounters         |

---

## Skills Applied

### Database Design

- **Normalization**: I designed 3NF schema to reduce redundancy
- **Entity Relationships**: Built 8 tables with 2 junction tables for many-to-many relationships
- **Referential Integrity**: Implemented 12 foreign key constraints with cascading actions
- **Indexing**: Optimized primary/foreign keys for multi-table joins

### SQL Techniques

| Category              | What I Applied                                |
| --------------------- | --------------------------------------------- |
| **Joins**             | Multi-table (4+), LEFT/INNER, self-joins      |
| **Advanced Queries**  | CTEs, correlated subqueries, window functions |
| **Temporal Analysis** | DATEDIFF, DATE_ADD for 30-day tracking        |
| **Aggregation**       | GROUP BY + HAVING, CASE for categorization    |

### Data Integration

- **Python-MySQL**: Established database connectivity with Pandas for preprocessing
- **ETL**: Executed LOAD DATA INFILE bulk import from CSV
- **Data Validation**: Verified record counts against AUTO_INCREMENT values

---

## Technologies Used

**Database**: MySQL 8.0  
**Languages**: SQL, Python  
**Libraries**: Pandas (ETL preprocessing)  
**Data Source**: Synthea synthetic EHR data

---

## Academic Information

**Course**: INFO 579 - SQL & NoSQL Databases  
**Institution**: University of Arizona  
**Term**: 2024-2025  
**Program**: Graduate Student — M.S. in Data Science

---

<p align="center">
  <em>Database design and SQL analytics for healthcare data</em>
</p>
