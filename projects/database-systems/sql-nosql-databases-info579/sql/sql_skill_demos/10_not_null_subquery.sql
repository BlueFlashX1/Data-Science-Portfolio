-- ============================================================
-- INFO 579 Final Project · Section 8.10: NOT NULL OPERATOR SUBQUERY
-- Demonstrates: IN subquery filtering on IS NOT NULL to count encounters for deceased patients
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write a subquery using the NOT NULL operator in the inner query. Show the results and
--   sort the results by key field(s). Interpret the output.

SELECT
  e.encounter_class,
  COUNT(*) AS n_encounters_deceased
FROM encounter e
WHERE e.patient_id IN (
  SELECT patient_id
  FROM patient
  WHERE death_date IS NOT NULL
)
GROUP BY e.encounter_class
ORDER BY n_encounters_deceased DESC, e.encounter_class;
