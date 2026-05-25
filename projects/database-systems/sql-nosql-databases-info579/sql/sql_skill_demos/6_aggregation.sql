-- ============================================================
-- INFO 579 Final Project · Section 8.6: AGGREGATION
-- Demonstrates: multi-column GROUP BY aggregation of procedure counts per provider/specialty
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write an SQL to aggregate the results by using multiple columns in the SELECT clause.
--   Interpret the output.

SELECT pr.provider_id,
       pr.provider_specialty,
       COUNT(pc.procedure_id) AS total_procedures
FROM provider pr
LEFT JOIN encounter e
  ON pr.provider_id = e.provider_id
  AND pr.organization_id = e.organization_id
LEFT JOIN procedures pc
  ON pc.encounter_id = e.encounter_id
GROUP BY pr.provider_id, pr.provider_specialty
ORDER BY total_procedures DESC;
