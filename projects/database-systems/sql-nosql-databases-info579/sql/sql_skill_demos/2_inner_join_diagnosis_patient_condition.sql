-- ============================================================
-- INFO 579 Final Project · Section 8.2: INNER JOIN
-- Demonstrates: junction table joining diagnosis <-> patient <-> medical_condition
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write an SQL involving the junction table and two other related tables.
--   You must use the INNER JOIN to connect with all three tables.
--   The database that you created must be included in your SQL queries.

DROP TABLE IF EXISTS Final_Project.rpt_diagnosis_patient_condition;

CREATE TABLE Final_Project.rpt_diagnosis_patient_condition AS
SELECT
  d.patient_id,
  p.first_name,
  p.last_name,
  mc.condition_id,
  mc.condition_code,
  mc.condition_description
FROM Final_Project.diagnosis AS d
INNER JOIN Final_Project.patient AS p
  ON p.patient_id = d.patient_id
INNER JOIN Final_Project.medical_condition AS mc
  ON mc.condition_id = d.condition_id;

SELECT *
FROM Final_Project.rpt_diagnosis_patient_condition
ORDER BY patient_id, condition_id;

-- top 10 conditions by DISTINCT patients (prevalence)
SELECT
  condition_description,
  COUNT(DISTINCT patient_id) AS n_patients
FROM Final_Project.rpt_diagnosis_patient_condition
GROUP BY condition_description
ORDER BY n_patients DESC, condition_description
LIMIT 10;
