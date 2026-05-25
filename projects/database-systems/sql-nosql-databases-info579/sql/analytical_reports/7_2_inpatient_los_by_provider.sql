-- ============================================================
-- INFO 579 Final Project · Section 7.2: Inpatient length of stay
--   (average LOS in days per provider, inpatient encounters only)
-- Source: Matthew Thompson's final report PDF (page 16)
-- ============================================================

DROP TABLE IF EXISTS rpt_inpatient_los_provider;

CREATE TABLE rpt_inpatient_los_provider AS
SELECT pr.provider_id,
       pr.organization_id,
       pr.provider_name,
       ROUND(AVG(TIMESTAMPDIFF(HOUR, e.encounter_start_date,
         e.encounter_end_date)) / 24, 2) AS avg_los_days,
       COUNT(*) AS n_inpatient_encounters
FROM encounter e
JOIN provider pr
  ON pr.provider_id = e.provider_id
  AND pr.organization_id = e.organization_id
WHERE LOWER(e.encounter_class) = 'inpatient'
  AND e.encounter_end_date IS NOT NULL
GROUP BY pr.provider_id, pr.organization_id, pr.provider_name;

SELECT * FROM rpt_inpatient_los_provider
ORDER BY avg_los_days DESC, provider_id;
