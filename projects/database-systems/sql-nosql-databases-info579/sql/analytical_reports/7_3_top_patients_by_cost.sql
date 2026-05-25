-- ============================================================
-- INFO 579 Final Project · Section 7.3: Top patients by total claim cost
--   (top 10 patients ranked by sum of all encounter claim costs)
-- Source: Matthew Thompson's final report PDF (page 17)
-- ============================================================

SELECT p.patient_id,
       p.first_name,
       p.last_name,
       SUM(e.total_claim_cost) AS total_claim_cost
FROM patient p
JOIN encounter e ON e.patient_id = p.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name
ORDER BY total_claim_cost DESC, p.patient_id
LIMIT 10;
