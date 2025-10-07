# Healthcare Analytics Database Backup

[![Database](https://img.shields.io/badge/Database-MySQL_8.0-blue?style=for-the-badge&logo=mysql)](https://mysql.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)](https://docker.com)
[![Healthcare](https://img.shields.io/badge/Domain-Healthcare_Analytics-green?style=for-the-badge)](https://github.com)

> **Database backup from INFO 579 Final Project demonstrating advanced SQL analytics on synthetic healthcare data**

## 🗃️ Database Files

| File | Size | Description | Safe for GitHub |
|------|------|-------------|-----------------|
| [`Final_Project_schema.sql`](./Final_Project_schema.sql) | 18KB | **Complete database structure** - Tables, indexes, relationships | ✅ **YES** |
| [`Final_Project_analytics_reports.sql`](./Final_Project_analytics_reports.sql) | 3.4MB | **Analytics report tables** - Aggregated healthcare insights | ✅ **YES** |
| [`Final_Project_sample_data.sql`](./Final_Project_sample_data.sql) | 74KB | **Sample patient data** (100 records) - Limited dataset for demo | ⚠️ **CAUTION** |

## 🔒 Privacy & Security Considerations

### ✅ **Safe to Share (Recommended for GitHub):**
- **Database Schema** (`Final_Project_schema.sql`)
  - Shows database design expertise
  - No patient data included
  - Demonstrates complex relationship modeling
  
- **Analytics Reports** (`Final_Project_analytics_reports.sql`)
  - Aggregated statistics and insights
  - No individual patient identifiers
  - Shows advanced SQL analytical capabilities

### ⚠️ **Use Caution:**
- **Sample Data** (`Final_Project_sample_data.sql`)
  - Contains synthetic patient records (Synthea generated)
  - Even though synthetic, contains detailed personal information
  - Consider excluding from public repositories

## 📊 Database Structure

### Core Tables
- `patient` - Patient demographics and information
- `encounter` - Medical visits and appointments  
- `diagnosis` - Medical diagnoses and conditions
- `procedures` - Medical procedures and treatments
- `provider` - Healthcare providers and facilities
- `treatment` - Treatment records
- `observation` - Clinical measurements and test results

### Analytics Reports (13 tables)
- `rpt_condition_prevalence` - Disease prevalence analysis
- `rpt_readmissions_30d` - 30-day readmission tracking
- `rpt_provider_utilization` - Provider performance metrics
- `rpt_encounter_activity` - Visit activity patterns
- `rpt_er_frequenters` - Emergency room usage analysis
- `rpt_procedure_costs` - Procedure cost analysis
- And 7 additional analytical reports

## 🚀 Database Restoration

### Prerequisites
```bash
# MySQL 8.0 or compatible
mysql --version

# Or Docker with MySQL
docker --version
```

### Restore Schema Only (Recommended for demos)
```sql
-- Create database
CREATE DATABASE healthcare_demo;

-- Import schema
mysql -u root -p healthcare_demo < Final_Project_schema.sql

-- Import analytics (no personal data)
mysql -u root -p healthcare_demo < Final_Project_analytics_reports.sql
```

### Full Restore (with sample data)
```sql
-- Create database
CREATE DATABASE healthcare_full;

-- Import everything
mysql -u root -p healthcare_full < Final_Project_schema.sql
mysql -u root -p healthcare_full < Final_Project_analytics_reports.sql
mysql -u root -p healthcare_full < Final_Project_sample_data.sql
```

### Docker Container Setup
```bash
# Run MySQL container
docker run -d \
  --name healthcare_analytics \
  -e MYSQL_ROOT_PASSWORD=your_password \
  -e MYSQL_DATABASE=healthcare_demo \
  -p 3306:3306 \
  mysql:8.0

# Restore database
docker exec -i healthcare_analytics mysql -u root -pyour_password healthcare_demo < Final_Project_schema.sql
```

## 🎯 Key Analytics Demonstrations

### Sample Queries You Can Run

```sql
-- Condition prevalence analysis
SELECT condition_description, n_patients 
FROM rpt_condition_prevalence 
ORDER BY n_patients DESC 
LIMIT 10;

-- 30-day readmission patterns
SELECT patient_id, COUNT(*) as readmission_count
FROM rpt_readmissions_30d 
GROUP BY patient_id 
HAVING readmission_count > 2;

-- Provider utilization metrics
SELECT * FROM rpt_provider_utilization 
WHERE utilization_score > 0.8;
```

## 🛡️ Data Privacy Notes

### Synthetic Data Source
- All patient data generated using **Synthea** (synthetic patient generator)
- No real patient information included
- Follows realistic healthcare data patterns for analysis

### GitHub Recommendations
**✅ Include in Portfolio:**
- Database schema (shows design skills)
- Analytics reports (demonstrates SQL expertise)
- This README with usage examples

**❌ Consider Excluding:**
- Raw patient data (even if synthetic, contains PII-like structure)
- Large data dumps (repository size)
- Database credentials or connection strings

## 🔧 Technical Achievements Demonstrated

### Advanced SQL Skills
- **Complex Joins**: Multi-table healthcare relationship queries
- **Window Functions**: Advanced analytical calculations
- **Stored Procedures**: Automated report generation
- **Triggers**: Data integrity enforcement
- **Indexes**: Performance optimization

### Healthcare Domain Expertise
- **Medical Coding**: ICD-10, CPT procedure codes
- **Clinical Workflows**: Patient care pathway modeling
- **Population Health**: Epidemiological analysis patterns
- **Quality Metrics**: Healthcare performance indicators

### Database Administration
- **Schema Design**: Normalized healthcare data model
- **Performance Tuning**: Optimized queries for large datasets
- **Docker Deployment**: Containerized database solution
- **Backup & Recovery**: Database maintenance procedures

## 📈 Portfolio Impact

This database backup demonstrates:
- **Enterprise-level database design** skills
- **Healthcare informatics** expertise
- **Advanced SQL analytical** capabilities
- **Docker containerization** proficiency
- **Real-world data modeling** experience

Perfect for showcasing to potential employers in:
- Healthcare technology companies
- Data engineering roles
- Database administration positions
- Healthcare analytics organizations

---

<div align="center">

**Synthetic healthcare data used for educational and portfolio demonstration purposes**

*Demonstrating advanced database design and healthcare analytics capabilities*

</div>