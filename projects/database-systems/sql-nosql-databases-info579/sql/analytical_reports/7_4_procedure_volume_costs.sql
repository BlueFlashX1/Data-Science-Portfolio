-- ============================================================
-- INFO 579 Final Project · Section 7.4: Procedure volume & average base cost
--   (count of procedures and avg base cost per procedure code, top 25 by volume)
-- Source: Matthew Thompson's final report PDF (page 17)
-- ============================================================

CREATE TABLE rpt_procedure_costs AS
SELECT prc.procedure_code,
       prc.procedure_description,
       COUNT(*) AS n_procedures,
       ROUND(AVG(prc.procedure_base_cost), 2) AS avg_base_cost
FROM procedures prc
GROUP BY prc.procedure_code, prc.procedure_description;

SELECT * FROM rpt_procedure_costs
ORDER BY n_procedures DESC, procedure_code
LIMIT 25;
