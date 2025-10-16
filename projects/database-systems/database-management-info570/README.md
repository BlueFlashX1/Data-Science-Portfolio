# Cross-Platform SQL Database Implementation

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 570](https://img.shields.io/badge/INFO%20570-Database%20Management-red?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

> **Multi-platform SQL implementation demonstrating database design and cross-platform development** • University of Arizona, INFO 570

Implemented normalized database schemas across MySQL and SQL Server for retail (KIMTAY) and healthcare (STAYWELL) applications. Demonstrates comprehensive SQL skills (DDL, DML, complex queries), database design principles (3NF normalization, ER modeling), and cross-platform SQL development.

**Tech Stack**: MySQL • SQL Server • Cross-Platform SQL • Database Design

---

## SQL Implementations

| Platform | Database | Script | Lines | Description |
|----------|----------|--------|-------|-------------|
| **MySQL** | KIMTAY | [`KIMTAY_SCRIPT_MYSQL.sql`](./sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_MYSQL.sql) | 122 | Pet store retail management |
| **MySQL** | STAYWELL | [`STAYWELL_SCRIPT_MYSQL.sql`](./sql-scripts/SQL10e_Module3_STAYWELL_SCRIPT_MYSQL.sql) | 157 | Healthcare property management |
| **SQL Server** | KIMTAY | [`KIMTAY_SCRIPT_SQLSERVER.sql`](./sql-scripts/SQL10e_Module3_KIMTAY_SCRIPT_SQLSERVER.sql) | 124 | SQL Server T-SQL version |

**Total: 403 lines of SQL code across 3 implementations**

### Skills Demonstrated

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)

**Core Competencies**:

- **Multi-Platform SQL**: MySQL and SQL Server (T-SQL) development
- **Database Design**: Third Normal Form (3NF) normalization, ER modeling
- **Referential Integrity**: Primary keys, foreign keys, constraint implementation
- **SQL Proficiency**: DDL (CREATE, ALTER, DROP), DML (INSERT, UPDATE, DELETE), complex queries
- **Business Domains**: Retail management (KIMTAY), healthcare services (STAYWELL)

---

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

- Healthcare domain schema for service operations
- Patient registration, service scheduling, provider coordination
- Database design for healthcare data management
- Normalized design supporting healthcare practice needs

---

## Sample SQL Implementations

### KIMTAY Schema Example

```sql
-- Core business entities with referential integrity
CREATE TABLE SALES_REP (
  REP_ID INT PRIMARY KEY,
  FIRST_NAME VARCHAR(50),
  LAST_NAME VARCHAR(50),
  COMMISSION DECIMAL(10,2),
  RATE DECIMAL(5,3)
);

CREATE TABLE CUSTOMER (
  CUST_ID INT PRIMARY KEY,
  FIRST_NAME VARCHAR(50),
  LAST_NAME VARCHAR(50),
  BALANCE DECIMAL(10,2),
  CREDIT_LIMIT DECIMAL(10,2),
  REP_ID INT,
  FOREIGN KEY (REP_ID) REFERENCES SALES_REP(REP_ID)
);
```

### Business Intelligence Query Example

```sql
-- Customer sales analysis with multi-table joins
SELECT 
  c.FIRST_NAME, 
  c.LAST_NAME, 
  SUM(il.QUANTITY * il.QUOTED_PRICE) as TOTAL_SALES
FROM CUSTOMER c
JOIN INVOICES i ON c.CUST_ID = i.CUST_ID
JOIN INVOICE_LINE il ON i.INVOICE_NUM = il.INVOICE_NUM
GROUP BY c.CUST_ID, c.FIRST_NAME, c.LAST_NAME
ORDER BY TOTAL_SALES DESC;
```

### Inventory Management Query

```sql
-- Low inventory alert system
SELECT ITEM_ID, DESCRIPTION, ON_HAND, CATEGORY
FROM ITEM 
WHERE ON_HAND < 15
ORDER BY ON_HAND ASC;
```

---

## Project Structure

```
database-management-info570/
├── README.md                                          # Project documentation
├── SC_AC19_9a_MatthewThompson_2.accdb                # Microsoft Access database
└── sql-scripts/                                      # SQL implementations
    ├── SQL10e_Module3_KIMTAY_SCRIPT_MYSQL.sql       # KIMTAY (MySQL)
    ├── SQL10e_Module3_KIMTAY_SCRIPT_SQLSERVER.sql    # KIMTAY (SQL Server)
    └── SQL10e_Module3_STAYWELL_SCRIPT_MYSQL.sql     # STAYWELL (MySQL)
```

---

## Technologies

**Database Platforms**: MySQL 8.0 • SQL Server • Microsoft Access  
**SQL Skills**: DDL • DML • Complex Joins • Subqueries • Aggregation  
**Design Principles**: 3NF Normalization • ER Modeling • Referential Integrity  
**Domains**: Retail Management • Healthcare Services

---

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.