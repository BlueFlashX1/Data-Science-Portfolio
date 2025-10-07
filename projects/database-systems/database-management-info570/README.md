# Database Management Systems

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 570](https://img.shields.io/badge/INFO%20570-Database%20Management-red?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

[![SQL](https://img.shields.io/badge/SQL-Multi%20Platform-4479A1?style=flat-square&logo=postgresql)](https://postgresql.org)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql)](https://mysql.com)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-Database-CC2927?style=flat-square&logo=microsoft-sql-server)](https://microsoft.com)
[![Access](https://img.shields.io/badge/Microsoft%20Access-Database-A4373A?style=flat-square&logo=microsoft-access)](https://microsoft.com)

> **COURSE PROJECT COLLECTION**: Database design and implementation across multiple platforms demonstrating comprehensive database management skills

**Academic Context**: This is a project collection for INFO 570 (Database Management) showcasing practical database design, implementation, and administration skills across multiple database management systems.

## Project Overview

This collection demonstrates comprehensive database management expertise through hands-on implementation of normalized database schemas, cross-platform SQL development, and professional database administration practices.

### Key Learning Outcomes
- Multi-platform Database Development: MySQL, SQL Server, Microsoft Access
- Database Design Principles: Normalization, ER modeling, constraint implementation
- SQL Proficiency: DDL, DML, complex queries across different SQL dialects
- Database Administration: Schema management, data integrity, performance considerations
- Business Applications: Real-world database scenarios and implementations

## Project Components

### SQL Database Implementations

| Database System | Script Files | Size | Description |
|----------------|--------------|------|-------------|
| MySQL | [`KIMTAY_SCRIPT_MYSQL.sql`](./sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_MYSQL.sql) | 6.6KB | Complete KIMTAY pet store database with normalized schema |
| MySQL | [`STAYWELL_SCRIPT_MYSQL.sql`](./sql-scripts/SQL10e_Module3_STAYWELL_SCRIPT_MYSQL.sql) | 8.4KB | STAYWELL health services database system |
| SQL Server | [`KIMTAY_SCRIPT_SQLSERVER.sql`](./sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_SQLSERVER.sql) | 6.7KB | SQL Server optimized version of KIMTAY database |

### Microsoft Access Database Projects

| File | Size | Description |
|------|------|-------------|
| [`SC_AC19_9a_MatthewThompson_2.accdb`](./SC_AC19_9a_MatthewThompson_2.accdb) | 1.7MB | Advanced Access database with complex forms, reports, and queries |

### Course Reflection

| File | Size | Description |
|------|------|-------------|
| [`INFO 570 Reflection Essay.docx`](./INFO%20570%20Reflection%20Essay.docx) | 25KB | Comprehensive reflection on database management learning outcomes |

## Database Implementations

### KIMTAY Pet Store Database System
Complete retail management system for pet store operations including inventory management, customer tracking, and sales processing.

### STAYWELL Health Services Database
Healthcare service management and patient coordination system with specialized schema for health service operations.

## Technical Implementation

Cross-platform database development with MySQL and SQL Server implementations, featuring normalized database design and comprehensive referential integrity.

## Usage Instructions

### MySQL Database Deployment
```bash
# Connect to MySQL server
mysql -u username -p

# Create and populate KIMTAY database
source sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_MYSQL.sql

# Create and populate STAYWELL database  
source sql-scripts/SQL10e_Module3_STAYWELL_SCRIPT_MYSQL.sql
```

### SQL Server Database Deployment
```bash
# Using SQL Server command line
sqlcmd -S server_name -d database_name -i sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_SQLSERVER.sql
```

### Microsoft Access Database
```
# Open with Microsoft Access
1. Double-click SC_AC19_9a_MatthewThompson_2.accdb
2. Enable macros if prompted
3. Navigate through forms and reports to explore functionality
```

## Advanced SQL Analysis

| Technique | Application |
|-----------|-------------|
| Complex Multi-table Joins | Combining customer, invoice, and product data across normalized tables |
| Aggregate Functions | Sales totals, inventory counts, customer metrics |
| Grouping and Filtering | Sales performance by representative, inventory analysis |
| Subqueries | Nested analysis for business intelligence reporting |
| Cross-Platform SQL | MySQL and SQL Server implementations with dialect optimization |
| Referential Integrity | Foreign key constraints and cascading operations |
| Performance Optimization | Indexing strategies and query optimization |
| Data Normalization | Third Normal Form implementation across business entities |

## Project Structure

```
database-management-info570/
├── README.md                                          # This documentation
├── INFO 570 Reflection Essay.docx                    # Course reflection and analysis
├── SC_AC19_9a_MatthewThompson_2.accdb                # Microsoft Access database project
└── sql-scripts/                                      # SQL database implementations
    ├── SQL10e_Module3_KIMTAY_SCRIPT_MYSQL.sql       # KIMTAY pet store (MySQL)
    ├── SQL10e_Module3_KIMTAY_SCRIPT_SQLSERVER.sql    # KIMTAY pet store (SQL Server)
    └── SQL10e_Module3_STAYWELL_SCRIPT_MYSQL.sql     # STAYWELL health services (MySQL)
```

## Core Technologies

- Multi-Platform Development: MySQL, SQL Server, Microsoft Access
- Enterprise Database Design: Normalized schemas with complete referential integrity
- Business Intelligence: Sales analysis, inventory management, performance tracking
- Database Administration: Schema management, constraint implementation, optimization

## File Recommendations

For Database Implementation: Use the [`sql-scripts/`](./sql-scripts/) directory - contains production-ready database schemas that can be immediately deployed.

For Access Development: Open [`SC_AC19_9a_MatthewThompson_2.accdb`](./SC_AC19_9a_MatthewThompson_2.accdb) - demonstrates advanced Access features including forms, reports, and complex queries.

For Learning Reflection: Review [`INFO 570 Reflection Essay.docx`](./INFO%20570%20Reflection%20Essay.docx) - comprehensive analysis of database management learning outcomes and professional growth.

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.

---

<div align="center">

**Database management expertise demonstrated through multi-platform implementations**

*Professional database design and administration across industry-standard platforms*

</div>