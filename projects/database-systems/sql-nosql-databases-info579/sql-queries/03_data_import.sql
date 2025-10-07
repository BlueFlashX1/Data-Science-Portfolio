-- Healthcare Data Import Script
-- INFO 579 - SQL & NoSQL Databases  
-- Loading CSV data into healthcare database tables

-- ==================================================
-- LOAD PATIENT DATA
-- ==================================================

-- Load patients from CSV (MySQL syntax)
LOAD DATA INFILE 'data/patients.csv'
INTO TABLE patients
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, birthdate, @deathdate, ssn, drivers, passport, prefix, 
 first_name, last_name, suffix, maiden, marital, race, ethnicity, 
 gender, birthplace, address, city, state, county, zip, 
 lat, lon, healthcare_expenses, healthcare_coverage)
SET deathdate = NULLIF(@deathdate, '');

-- Alternative for PostgreSQL or other databases:
/*
COPY patients FROM 'data/patients.csv' 
DELIMITER ',' CSV HEADER;
*/

-- ==================================================
-- LOAD CONDITION DATA
-- ==================================================

-- Load conditions from CSV
LOAD DATA INFILE 'data/conditions.csv'
INTO TABLE conditions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@start_date, @stop_date, patient_id, encounter_id, code, description)
SET 
    start_date = STR_TO_DATE(@start_date, '%Y-%m-%d'),
    stop_date = CASE WHEN @stop_date = '' THEN NULL ELSE STR_TO_DATE(@stop_date, '%Y-%m-%d') END;

-- ==================================================
-- LOAD PROVIDER DATA  
-- ==================================================

-- Load providers from CSV
LOAD DATA INFILE 'data/providers.csv'
INTO TABLE providers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- ==================================================
-- POST-IMPORT DATA VALIDATION
-- ==================================================

-- Verify data import counts
SELECT 'patients' as table_name, COUNT(*) as record_count FROM patients
UNION ALL
SELECT 'conditions' as table_name, COUNT(*) as record_count FROM conditions  
UNION ALL
SELECT 'providers' as table_name, COUNT(*) as record_count FROM providers;

-- Check for any import errors or data quality issues
SELECT 
    'Invalid patient birthdates' as issue_type,
    COUNT(*) as count
FROM patients 
WHERE birthdate > CURDATE() OR birthdate < '1900-01-01'

UNION ALL

SELECT 
    'Patients with future death dates' as issue_type,
    COUNT(*) as count  
FROM patients
WHERE deathdate > CURDATE()

UNION ALL

SELECT 
    'Conditions with invalid dates' as issue_type,
    COUNT(*) as count
FROM conditions
WHERE start_date > CURDATE() OR (stop_date IS NOT NULL AND stop_date < start_date);

-- ==================================================
-- CREATE SAMPLE VIEWS FOR ANALYSIS
-- ==================================================

-- Create a view for patient demographics with calculated fields
CREATE OR REPLACE VIEW patient_demographics AS
SELECT 
    p.id,
    p.first_name,
    p.last_name,
    p.birthdate,
    YEAR(CURDATE()) - YEAR(p.birthdate) as age,
    p.gender,
    p.race,
    p.ethnicity,
    p.state,
    p.healthcare_expenses,
    p.healthcare_coverage,
    ROUND(p.healthcare_coverage / NULLIF(p.healthcare_expenses, 0) * 100, 1) as coverage_percentage,
    CASE 
        WHEN p.deathdate IS NULL THEN 'Living'
        ELSE 'Deceased'
    END as status
FROM patients p;

-- Create a view for condition summary per patient
CREATE OR REPLACE VIEW patient_condition_summary AS
SELECT 
    p.id as patient_id,
    p.first_name,
    p.last_name,
    COUNT(DISTINCT c.code) as total_conditions,
    COUNT(CASE WHEN c.stop_date IS NULL THEN 1 END) as active_conditions,
    MIN(c.start_date) as first_condition_date,
    MAX(c.start_date) as latest_condition_date
FROM patients p
LEFT JOIN conditions c ON p.id = c.patient_id
GROUP BY p.id, p.first_name, p.last_name;

-- ==================================================
-- PERFORMANCE OPTIMIZATION
-- ==================================================

-- Update table statistics for query optimization
ANALYZE TABLE patients;
ANALYZE TABLE conditions;
ANALYZE TABLE providers;

-- Create additional indexes based on common query patterns
CREATE INDEX idx_patients_age ON patients(birthdate);
CREATE INDEX idx_patients_expenses ON patients(healthcare_expenses);
CREATE INDEX idx_conditions_start_date ON conditions(start_date);
CREATE INDEX idx_conditions_description ON conditions(description);

-- ==================================================
-- DATA SUMMARY STATISTICS
-- ==================================================

-- Generate summary statistics for validation
SELECT 
    'Data Import Summary' as summary_type,
    (SELECT COUNT(*) FROM patients) as total_patients,
    (SELECT COUNT(*) FROM conditions) as total_conditions,
    (SELECT COUNT(*) FROM providers) as total_providers,
    (SELECT COUNT(DISTINCT patient_id) FROM conditions) as patients_with_conditions,
    (SELECT AVG(healthcare_expenses) FROM patients) as avg_healthcare_expenses;