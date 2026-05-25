-- ============================================================
-- INFO 579 Final Project · Section 8.5: MULTIPLE-ROW SUBQUERY
-- Demonstrates: multi-row IN subquery identifying providers treating high-risk ER patients
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write a multiple-row subquery. Show the results and sort the results by key field(s).
--   Interpret the output.

CREATE TABLE rpt_providers_highrisk_er AS
WITH provider_tot AS (
  SELECT provider_id, organization_id, COUNT(*) AS total_encounters
  FROM encounter
  GROUP BY provider_id, organization_id
),
highrisk_patients AS (
  SELECT e.patient_id
  FROM encounter e
  WHERE LOWER(e.encounter_class) = 'emergency'
  GROUP BY e.patient_id
  HAVING COUNT(*) >= 10
)
SELECT
  pr.provider_id,
  pr.organization_id,
  pr.provider_name,
  pr.provider_specialty,
  COUNT(DISTINCT e.patient_id) AS n_highrisk_patients,
  COUNT(*) AS n_highrisk_encounters,
  pt.total_encounters,
  ROUND(100 * COUNT(*) / NULLIF(pt.total_encounters, 0), 2) AS pct_of_provider_encounters
FROM provider pr
JOIN encounter e
  ON e.provider_id = pr.provider_id
  AND e.organization_id = pr.organization_id
JOIN provider_tot pt
  ON pt.provider_id = pr.provider_id
  AND pt.organization_id = pr.organization_id
WHERE e.patient_id IN (SELECT patient_id FROM highrisk_patients) -- multi-row subquery use
GROUP BY
  pr.provider_id, pr.organization_id, pr.provider_name,
  pr.provider_specialty, pt.total_encounters;

SELECT *
FROM rpt_providers_highrisk_er
ORDER BY n_highrisk_encounters DESC;
