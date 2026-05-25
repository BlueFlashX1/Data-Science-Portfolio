-- ============================================================
-- INFO 579 Final Project · Section 7.6: High-risk frequent ER users
--   (patients with 3 or more emergency encounters, ranked by visit count)
-- Source: Matthew Thompson's final report PDF (page 19)
-- ============================================================

CREATE TABLE rpt_er_frequenters AS
SELECT p.patient_id,
       p.first_name,
       p.last_name,
       COUNT(*) AS er_visits
FROM encounter e
JOIN patient p
  ON p.patient_id = e.patient_id
WHERE LOWER(e.encounter_class) = 'emergency'
GROUP BY p.patient_id, p.first_name, p.last_name
HAVING COUNT(*) >= 3;

SELECT *
FROM rpt_er_frequenters
ORDER BY er_visits DESC, last_name, first_name, patient_id;
