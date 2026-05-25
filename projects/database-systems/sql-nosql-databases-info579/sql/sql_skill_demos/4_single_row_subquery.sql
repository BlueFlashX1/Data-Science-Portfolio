-- ============================================================
-- INFO 579 Final Project · Section 8.4: SINGLE-ROW SUBQUERY
-- Demonstrates: correlated single-row subquery using MAX() to find highest-cost patient
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write a single-row subquery. Show the results and sort the results by key field(s).
--   Interpret the output.

SELECT patient_id, first_name, last_name, patient_gender,
       patient_city, patient_state, healthcare_expenses, healthcare_coverage
FROM patient
WHERE healthcare_expenses = (SELECT MAX(healthcare_expenses) FROM patient)
ORDER BY patient_id;
