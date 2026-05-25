-- ============================================================
-- INFO 579 Final Project · Section 8.3: LEFT OUTER JOIN
-- Demonstrates: multi-table LEFT JOIN to expose encounters with no provider or procedures
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write an SQL statement by including two or more tables and using the LEFT OUTER
--   JOIN. Show the results and sort the results by key field(s). Interpret the results
--   compared to what an INNER JOIN does.

CREATE TABLE rpt_encounter_activity AS
SELECT
  e.encounter_id,
  e.patient_id,
  e.encounter_start_date,
  e.encounter_class,
  pr.provider_id,
  pr.organization_id,
  pr.provider_name,
  COUNT(pc.procedure_id) AS n_procedures
FROM encounter e
LEFT JOIN provider pr
  ON pr.provider_id = e.provider_id
  AND pr.organization_id = e.organization_id
LEFT JOIN procedures pc
  ON pc.encounter_id = e.encounter_id
GROUP BY
  e.encounter_id, e.patient_id, e.encounter_start_date, e.encounter_class,
  pr.provider_id, pr.organization_id, pr.provider_name;

SELECT
  encounter_id,
  encounter_class,
  provider_id,
  provider_name,
  n_procedures
FROM rpt_encounter_activity
WHERE provider_id IS NULL
ORDER BY encounter_id;
