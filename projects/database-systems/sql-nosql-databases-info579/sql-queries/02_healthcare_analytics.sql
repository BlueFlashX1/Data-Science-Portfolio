-- Healthcare Analytics Queries
-- INFO 579 - SQL & NoSQL Databases
-- Advanced analytical queries for healthcare data analysis

-- ==================================================
-- PATIENT DEMOGRAPHICS AND POPULATION HEALTH
-- ==================================================

-- Query 1: Patient age distribution and demographics
SELECT 
    CASE 
        WHEN YEAR(CURDATE()) - YEAR(birthdate) < 18 THEN 'Under 18'
        WHEN YEAR(CURDATE()) - YEAR(birthdate) BETWEEN 18 AND 30 THEN '18-30'
        WHEN YEAR(CURDATE()) - YEAR(birthdate) BETWEEN 31 AND 50 THEN '31-50'
        WHEN YEAR(CURDATE()) - YEAR(birthdate) BETWEEN 51 AND 70 THEN '51-70'
        ELSE 'Over 70'
    END AS age_group,
    gender,
    COUNT(*) as patient_count,
    AVG(healthcare_expenses) as avg_expenses,
    AVG(healthcare_coverage) as avg_coverage
FROM patients 
WHERE deathdate IS NULL  -- Only living patients
GROUP BY 
    CASE 
        WHEN YEAR(CURDATE()) - YEAR(birthdate) < 18 THEN 'Under 18'
        WHEN YEAR(CURDATE()) - YEAR(birthdate) BETWEEN 18 AND 30 THEN '18-30'
        WHEN YEAR(CURDATE()) - YEAR(birthdate) BETWEEN 31 AND 50 THEN '31-50'
        WHEN YEAR(CURDATE()) - YEAR(birthdate) BETWEEN 51 AND 70 THEN '51-70'
        ELSE 'Over 70'
    END, gender
ORDER BY age_group, gender;

-- Query 2: Geographic distribution of patients and healthcare expenses
SELECT 
    state,
    COUNT(*) as patient_count,
    AVG(healthcare_expenses) as avg_expenses,
    SUM(healthcare_expenses) as total_expenses,
    AVG(healthcare_coverage) as avg_coverage_ratio
FROM patients 
GROUP BY state
HAVING COUNT(*) >= 10  -- States with at least 10 patients
ORDER BY total_expenses DESC;

-- ==================================================
-- CONDITION ANALYSIS AND COMORBIDITY PATTERNS
-- ==================================================

-- Query 3: Most common conditions and their prevalence
SELECT 
    c.code,
    c.description,
    COUNT(DISTINCT c.patient_id) as patient_count,
    COUNT(*) as total_occurrences,
    ROUND(COUNT(DISTINCT c.patient_id) * 100.0 / (SELECT COUNT(*) FROM patients), 2) as prevalence_percentage
FROM conditions c
GROUP BY c.code, c.description
HAVING COUNT(DISTINCT c.patient_id) >= 5
ORDER BY patient_count DESC
LIMIT 20;

-- Query 4: Patients with multiple conditions (comorbidity analysis)
WITH patient_condition_counts AS (
    SELECT 
        patient_id,
        COUNT(DISTINCT code) as condition_count
    FROM conditions
    GROUP BY patient_id
)
SELECT 
    CASE 
        WHEN condition_count = 1 THEN '1 condition'
        WHEN condition_count BETWEEN 2 AND 3 THEN '2-3 conditions'
        WHEN condition_count BETWEEN 4 AND 6 THEN '4-6 conditions'
        ELSE '7+ conditions'
    END as condition_category,
    COUNT(*) as patient_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM patient_condition_counts
GROUP BY 
    CASE 
        WHEN condition_count = 1 THEN '1 condition'
        WHEN condition_count BETWEEN 2 AND 3 THEN '2-3 conditions'
        WHEN condition_count BETWEEN 4 AND 6 THEN '4-6 conditions'
        ELSE '7+ conditions'
    END
ORDER BY patient_count DESC;

-- Query 5: Condition co-occurrence analysis (conditions that occur together)
SELECT 
    c1.description as condition_1,
    c2.description as condition_2,
    COUNT(*) as co_occurrence_count
FROM conditions c1
JOIN conditions c2 ON c1.patient_id = c2.patient_id AND c1.code < c2.code
GROUP BY c1.code, c1.description, c2.code, c2.description
HAVING COUNT(*) >= 3
ORDER BY co_occurrence_count DESC
LIMIT 15;

-- ==================================================
-- TEMPORAL ANALYSIS AND HEALTHCARE UTILIZATION
-- ==================================================

-- Query 6: Seasonal patterns in condition onset
SELECT 
    MONTH(start_date) as month_num,
    MONTHNAME(start_date) as month_name,
    COUNT(*) as condition_count,
    COUNT(DISTINCT patient_id) as affected_patients
FROM conditions
WHERE start_date IS NOT NULL
GROUP BY MONTH(start_date), MONTHNAME(start_date)
ORDER BY month_num;

-- Query 7: Chronic vs acute conditions analysis
SELECT 
    CASE 
        WHEN stop_date IS NULL OR DATEDIFF(IFNULL(stop_date, CURDATE()), start_date) > 180 
        THEN 'Chronic'
        ELSE 'Acute'
    END as condition_type,
    COUNT(*) as condition_count,
    COUNT(DISTINCT patient_id) as patient_count,
    AVG(DATEDIFF(IFNULL(stop_date, CURDATE()), start_date)) as avg_duration_days
FROM conditions
WHERE start_date IS NOT NULL
GROUP BY 
    CASE 
        WHEN stop_date IS NULL OR DATEDIFF(IFNULL(stop_date, CURDATE()), start_date) > 180 
        THEN 'Chronic'
        ELSE 'Acute'
    END;

-- ==================================================
-- HEALTHCARE COST AND UTILIZATION ANALYSIS
-- ==================================================

-- Query 8: High-cost patients and their conditions
SELECT 
    p.id,
    p.first_name,
    p.last_name,
    p.healthcare_expenses,
    COUNT(DISTINCT c.code) as condition_count,
    GROUP_CONCAT(DISTINCT SUBSTRING(c.description, 1, 50) SEPARATOR '; ') as conditions_summary
FROM patients p
JOIN conditions c ON p.id = c.patient_id
WHERE p.healthcare_expenses > (
    SELECT AVG(healthcare_expenses) + 2 * STDDEV(healthcare_expenses) 
    FROM patients
)
GROUP BY p.id, p.first_name, p.last_name, p.healthcare_expenses
ORDER BY p.healthcare_expenses DESC;

-- Query 9: Healthcare coverage gap analysis
SELECT 
    CASE 
        WHEN healthcare_coverage / healthcare_expenses >= 0.9 THEN 'Well Covered (90%+)'
        WHEN healthcare_coverage / healthcare_expenses >= 0.7 THEN 'Adequately Covered (70-89%)'
        WHEN healthcare_coverage / healthcare_expenses >= 0.5 THEN 'Under Covered (50-69%)'
        ELSE 'Poorly Covered (<50%)'
    END as coverage_category,
    COUNT(*) as patient_count,
    AVG(healthcare_expenses) as avg_expenses,
    AVG(healthcare_coverage) as avg_coverage,
    AVG(healthcare_expenses - healthcare_coverage) as avg_out_of_pocket
FROM patients 
WHERE healthcare_expenses > 0
GROUP BY 
    CASE 
        WHEN healthcare_coverage / healthcare_expenses >= 0.9 THEN 'Well Covered (90%+)'
        WHEN healthcare_coverage / healthcare_expenses >= 0.7 THEN 'Adequately Covered (70-89%)'
        WHEN healthcare_coverage / healthcare_expenses >= 0.5 THEN 'Under Covered (50-69%)'
        ELSE 'Poorly Covered (<50%)'
    END
ORDER BY avg_out_of_pocket DESC;

-- ==================================================
-- DATA QUALITY AND INTEGRITY CHECKS
-- ==================================================

-- Query 10: Data quality assessment
SELECT 
    'Patients' as table_name,
    COUNT(*) as total_records,
    SUM(CASE WHEN first_name IS NULL THEN 1 ELSE 0 END) as missing_first_name,
    SUM(CASE WHEN last_name IS NULL THEN 1 ELSE 0 END) as missing_last_name,
    SUM(CASE WHEN birthdate IS NULL THEN 1 ELSE 0 END) as missing_birthdate,
    SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) as missing_gender
FROM patients

UNION ALL

SELECT 
    'Conditions' as table_name,
    COUNT(*) as total_records,
    SUM(CASE WHEN patient_id IS NULL THEN 1 ELSE 0 END) as missing_patient_id,
    SUM(CASE WHEN code IS NULL THEN 1 ELSE 0 END) as missing_code,
    SUM(CASE WHEN description IS NULL THEN 1 ELSE 0 END) as missing_description,
    SUM(CASE WHEN start_date IS NULL THEN 1 ELSE 0 END) as missing_start_date;

-- Query 11: Referential integrity check
SELECT 
    'Conditions without valid patient' as check_type,
    COUNT(*) as violation_count
FROM conditions c
LEFT JOIN patients p ON c.patient_id = p.id
WHERE p.id IS NULL

UNION ALL

SELECT 
    'Patients with no conditions' as check_type,
    COUNT(*) as count
FROM patients p
LEFT JOIN conditions c ON p.id = c.patient_id
WHERE c.patient_id IS NULL;