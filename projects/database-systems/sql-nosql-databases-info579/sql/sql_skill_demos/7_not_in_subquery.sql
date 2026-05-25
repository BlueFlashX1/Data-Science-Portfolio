-- ============================================================
-- INFO 579 Final Project · Section 8.7: NOT IN OPERATOR SUBQUERY
-- Demonstrates: NOT IN subquery to find patients with no diagnosis records
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write a subquery using the NOT IN operator. Show the results and sort the results by
--   key field(s). Interpret the output.

SELECT patient_id, first_name, last_name
FROM patient
WHERE patient_id NOT IN (SELECT DISTINCT patient_id FROM diagnosis)
ORDER BY first_name, last_name;
