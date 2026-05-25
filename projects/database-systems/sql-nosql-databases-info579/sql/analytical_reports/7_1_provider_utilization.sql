-- ============================================================
-- INFO 579 Final Project · Section 7.1: Provider utilization
--   (encounters per provider & specialty)
-- Source: Matthew Thompson's final report PDF (page 16)
-- ============================================================

DROP TABLE IF EXISTS rpt_provider_utilization;

CREATE TABLE rpt_provider_utilization AS
SELECT pr.provider_id,
       pr.organization_id,
       pr.provider_name,
       pr.provider_specialty,
       COUNT(e.encounter_id) AS n_encounters
FROM provider pr
LEFT JOIN encounter e
  ON e.provider_id = pr.provider_id
  AND e.organization_id = pr.organization_id
GROUP BY pr.provider_id, pr.organization_id, pr.provider_name, pr.provider_specialty;

SELECT * FROM rpt_provider_utilization
ORDER BY n_encounters DESC, provider_id;
