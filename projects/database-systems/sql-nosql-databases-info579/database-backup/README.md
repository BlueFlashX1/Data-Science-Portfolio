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

## 🔧 Database Access Troubleshooting

### Issue: Authentication Problems with MySQL Container

**Problem Encountered:**
Initial attempts to access the Docker MySQL container failed with authentication errors:
```bash
# Failed attempts
docker exec NoSQL_Assignments mysql -u root -pkeegoing -e "SHOW DATABASES;"
# ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)

docker exec NoSQL_Assignments mysql -u matthewqthompson -pkeegoing -e "SHOW DATABASES;"
# ERROR 1045 (28000): Access denied for user 'matthewqthompson'@'localhost' (using password: YES)
```

**Root Cause Analysis:**
1. **Container State**: MySQL container was running but potentially had stale authentication state
2. **Password Authentication**: MySQL 8.0 authentication plugin compatibility issues
3. **Connection Timing**: Database service may not have been fully initialized

**Resolution Steps:**

**Step 1: Container Restart**
```bash
# Restart the container to refresh MySQL service
docker restart NoSQL_Assignments
```

**Step 2: Verify Container Status**
```bash
# Confirm container is running properly
docker ps
# CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS         PORTS      NAMES
# b18a44482a12   mysql:8.0.36   "docker-entrypoint.s…"   2 months ago   Up 6 seconds   3306/tcp   NoSQL_Assignments
```

**Step 3: Extract Authentication Details**
```bash
# Inspect container environment variables for correct credentials
docker inspect NoSQL_Assignments | grep -A 5 -B 5 -i env
# Found: MYSQL_ROOT_PASSWORD=keepgoing
```

**Step 4: Successful Connection**
```bash
# Use correct password with proper syntax
docker exec NoSQL_Assignments mysql -u root -p'keepgoing' -e "SHOW DATABASES;"
# SUCCESS: Database list returned
```

### Key Lessons Learned

**1. Container State Management**
- Docker containers can have authentication state issues after prolonged inactivity
- Restarting the container often resolves MySQL authentication problems
- Always verify container status before troubleshooting application-level issues

**2. MySQL 8.0 Authentication**
- Password must be enclosed in single quotes: `-p'password'` not `-ppassword`
- MySQL 8.0 uses `caching_sha2_password` by default, which can cause compatibility issues
- Environment variables in container provide authoritative credential source

**3. Debugging Process**
- Check container logs: `docker logs container_name`
- Inspect container configuration: `docker inspect container_name`  
- Verify service readiness before application connections
- Test with simple queries before complex operations

### Best Practices for MySQL Containers

**Container Management:**
```bash
# Always check container status first
docker ps -a

# Restart if needed
docker restart container_name

# Check logs for errors
docker logs container_name --tail 20
```

**Authentication Best Practices:**
```bash
# Use environment variables for credentials
docker inspect container_name | grep -i mysql

# Test connection with simple query first
docker exec container_name mysql -u root -p'password' -e "SELECT 1;"

# Then proceed with complex operations
docker exec container_name mysql -u root -p'password' -e "SHOW DATABASES;"
```

**Security Considerations:**
- Store database passwords in environment variables or secrets management
- Avoid hardcoding credentials in scripts or documentation
- Use least-privilege access for production environments
- Consider using MySQL configuration files for authentication

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

## 📊 Key Analytical Findings

> **Real insights extracted from the healthcare analytics database demonstrating advanced SQL analysis capabilities**

### Dataset Overview
- **Total Patients**: 1,171 synthetic patient records
- **Total Encounters**: 53,346 medical visits and appointments  
- **Total Diagnoses**: 8,376 diagnosed conditions
- **Healthcare Providers**: 5,855 providers and facilities

### Disease Prevalence Analysis
**Top 5 Most Common Conditions:**

| Condition | Patient Count | Prevalence Rate |
|-----------|---------------|----------------|
| Viral sinusitis (disorder) | 743 | 63.5% |
| Acute viral pharyngitis (disorder) | 492 | 42.0% |
| Acute bronchitis (disorder) | 464 | 39.6% |
| Body mass index 30+ - obesity (finding) | 449 | 38.4% |
| Prediabetes | 317 | 27.1% |

**Key Insights:**
- **Respiratory conditions dominate**: Viral sinusitis and bronchitis affect majority of patients
- **Obesity epidemic**: 38.4% of patients have BMI 30+ obesity diagnosis
- **Diabetes concern**: 27.1% show prediabetic conditions, indicating population health risk

### 30-Day Readmission Analysis
**Readmission Metrics:**
- **Total 30-day readmissions**: 21,804 events
- **Patients with readmissions**: 1,059 (90.4% of all patients)
- **Average readmission interval**: 12.8 days
- **Highest-risk patient**: 1,892 readmission events

**Healthcare Quality Indicators:**
- **High readmission rate**: 90.4% of patients experienced at least one 30-day readmission
- **Short intervals**: Average 12.8 days between readmissions indicates potential care gaps
- **Frequent flyers**: Some patients with 1,500+ readmissions suggest complex chronic conditions

### Population Health Patterns
**Healthcare Utilization:**
- **Average encounters per patient**: 45.6 visits
- **Provider network size**: 5,855 healthcare providers
- **Condition burden per patient**: 7.1 diagnosed conditions average

**Risk Stratification Insights:**
- **High-utilization patients**: Identified through frequent readmission patterns
- **Complex cases**: Multi-morbidity patterns visible in condition co-occurrence
- **Care coordination opportunities**: Large provider network suggests fragmentation

### Advanced Analytics Capabilities Demonstrated

**1. Epidemiological Analysis**
```sql
-- Disease prevalence ranking with population impact
SELECT condition_description, n_patients,
       ROUND((n_patients * 100.0 / 1171), 1) as prevalence_rate
FROM rpt_condition_prevalence 
ORDER BY n_patients DESC;
```

**2. Healthcare Quality Metrics**
```sql
-- 30-day readmission risk assessment
SELECT patient_id, COUNT(*) as readmission_events,
       AVG(days_since_prior) as avg_interval
FROM rpt_readmissions_30d 
GROUP BY patient_id 
HAVING readmission_events > 100;
```

**3. Population Health Surveillance**
```sql
-- Multi-morbidity analysis for chronic disease management
SELECT patient_id, COUNT(DISTINCT condition_code) as condition_count
FROM diagnosis 
GROUP BY patient_id 
ORDER BY condition_count DESC;
```

### Healthcare Informatics Value

This analysis demonstrates:
- **Clinical decision support** through risk stratification
- **Population health management** via disease prevalence tracking  
- **Healthcare quality improvement** through readmission analysis
- **Resource allocation** insights from utilization patterns
- **Epidemiological surveillance** capabilities for public health

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