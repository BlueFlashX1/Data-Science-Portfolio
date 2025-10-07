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
- **Multi-platform Database Development**: MySQL, SQL Server, Microsoft Access
- **Database Design Principles**: Normalization, ER modeling, constraint implementation
- **SQL Proficiency**: DDL, DML, complex queries across different SQL dialects
- **Database Administration**: Schema management, data integrity, performance considerations
- **Business Applications**: Real-world database scenarios and implementations

## Project Components

### SQL Database Implementations

| Database System | Script Files | Size | Description |
|----------------|--------------|------|-------------|
| **MySQL** | [`KIMTAY_SCRIPT_MYSQL.sql`](./sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_MYSQL.sql) | 6.6KB | Complete KIMTAY pet store database with normalized schema |
| **MySQL** | [`STAYWELL_SCRIPT_MYSQL.sql`](./sql-scripts/SQL10e_Module3_STAYWELL_SCRIPT_MYSQL.sql) | 8.4KB | STAYWELL health services database system |
| **SQL Server** | [`KIMTAY_SCRIPT_SQLSERVER.sql`](./sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_SQLSERVER.sql) | 6.7KB | SQL Server optimized version of KIMTAY database |

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
**Business Context**: Complete retail management system for pet store operations

**Schema Design**:
```sql
-- Core business entities with referential integrity
SALES_REP (REP_ID, FIRST_NAME, LAST_NAME, COMMISSION, RATE)
CUSTOMER (CUST_ID, FIRST_NAME, LAST_NAME, BALANCE, CREDIT_LIMIT, REP_ID)
ITEM (ITEM_ID, DESCRIPTION, ON_HAND, CATEGORY, LOCATION, PRICE)
INVOICES (INVOICE_NUM, INVOICE_DATE, CUST_ID)
INVOICE_LINE (INVOICE_NUM, ITEM_ID, QUANTITY, QUOTED_PRICE)
```

**Key Features**:
- **Normalized Design**: Eliminates data redundancy through proper normalization
- **Referential Integrity**: Complete foreign key relationships and constraints
- **Business Logic**: Inventory management, customer tracking, sales processing
- **Real Data**: Populated with realistic business transactions and inventory

### STAYWELL Health Services Database
**Business Context**: Healthcare service management and patient coordination

**Key Features**:
- **Healthcare Domain**: Specialized schema for health service operations
- **Service Management**: Patient registration, service scheduling, provider coordination
- **Compliance**: Database design considerations for healthcare data management
- **Scalability**: Normalized design supporting growing healthcare practice needs

## Technical Implementation

### Cross-Platform SQL Development
**MySQL Implementation**:
- Optimized for MySQL-specific features and syntax
- Proper data type selection for MySQL environment
- MySQL-specific constraints and indexing strategies

**SQL Server Implementation**:
- Adapted for SQL Server T-SQL dialect
- SQL Server-specific data types and features
- Optimized for Windows/SQL Server environment

### Database Design Principles
- **Third Normal Form (3NF)**: Complete normalization to eliminate redundancy
- **Entity-Relationship Modeling**: Proper identification and modeling of business entities
- **Constraint Implementation**: Primary keys, foreign keys, check constraints
- **Data Integrity**: Comprehensive validation rules and referential integrity

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

## Sample Queries and Operations

### Business Intelligence Queries
```sql
-- Customer sales analysis
SELECT c.FIRST_NAME, c.LAST_NAME, SUM(il.QUANTITY * il.QUOTED_PRICE) as TOTAL_SALES
FROM CUSTOMER c
JOIN INVOICES i ON c.CUST_ID = i.CUST_ID
JOIN INVOICE_LINE il ON i.INVOICE_NUM = il.INVOICE_NUM
GROUP BY c.CUST_ID, c.FIRST_NAME, c.LAST_NAME
ORDER BY TOTAL_SALES DESC;

-- Inventory management
SELECT ITEM_ID, DESCRIPTION, ON_HAND, CATEGORY
FROM ITEM 
WHERE ON_HAND < 15
ORDER BY ON_HAND ASC;

-- Sales representative performance
SELECT sr.FIRST_NAME, sr.LAST_NAME, COUNT(c.CUST_ID) as CUSTOMER_COUNT, sr.COMMISSION
FROM SALES_REP sr
LEFT JOIN CUSTOMER c ON sr.REP_ID = c.REP_ID
GROUP BY sr.REP_ID, sr.FIRST_NAME, sr.LAST_NAME, sr.COMMISSION
ORDER BY CUSTOMER_COUNT DESC;
```

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

## Academic Information

**Course**: INFO 570 - Database Management  
**Institution**: University of Arizona  
**Project Type**: Multi-Module Course Projects  
**Focus Areas**: Database design, SQL development, cross-platform implementation  

### Skills Demonstrated
- **Database Design**: Complete ER modeling and normalization processes
- **Multi-Platform Development**: MySQL, SQL Server, Microsoft Access proficiency
- **SQL Proficiency**: Advanced query development and database manipulation
- **Business Application**: Real-world database scenarios and implementations
- **Professional Documentation**: Comprehensive project documentation and reflection

## Learning Outcomes

### Technical Mastery
- **Cross-Platform Compatibility**: Demonstrated ability to work across multiple database systems
- **SQL Dialect Expertise**: Proficient in MySQL and SQL Server T-SQL variations
- **Database Administration**: Schema management, constraint implementation, data integrity
- **Performance Considerations**: Optimized database design for query efficiency

### Professional Development
- **Business Analysis**: Translation of business requirements into database design
- **Project Management**: Multi-module project completion and documentation
- **Quality Assurance**: Thorough testing and validation of database implementations
- **Communication**: Clear technical documentation and reflection on learning process

## File Recommendations

**For Database Implementation**: Use the [`sql-scripts/`](./sql-scripts/) directory - contains production-ready database schemas that can be immediately deployed.

**For Access Development**: Open [`SC_AC19_9a_MatthewThompson_2.accdb`](./SC_AC19_9a_MatthewThompson_2.accdb) - demonstrates advanced Access features including forms, reports, and complex queries.

**For Learning Reflection**: Review [`INFO 570 Reflection Essay.docx`](./INFO%20570%20Reflection%20Essay.docx) - comprehensive analysis of database management learning outcomes and professional growth.

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.

---

<div align="center">

**Database management expertise demonstrated through multi-platform implementations**

*Professional database design and administration across industry-standard platforms*

</div>