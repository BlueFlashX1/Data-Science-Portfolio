-- ============================================================
-- INFO 579 Final Project · Section 7.5: Post-procedure follow-up within 14 days
--   (follow-up rate per procedure code — observation within 14 days of procedure)
-- Source: Matthew Thompson's final report PDF (pages 18–19)
-- ============================================================

DROP TABLE IF EXISTS rpt_followup_14d_by_proc_code;

CREATE TABLE rpt_followup_14d_by_proc_code AS
WITH proc_flags AS (
  SELECT prc.procedure_id,
         prc.procedure_code,
         prc.procedure_description,
         CASE
           WHEN EXISTS (
             SELECT 1
             FROM observation o
             WHERE o.patient_id = prc.patient_id
               AND o.observation_date > prc.procedure_date
               AND o.observation_date <= DATE_ADD(prc.procedure_date, INTERVAL 14 DAY)
           ) THEN 1 ELSE 0
         END AS has_followup_14d
  FROM procedures prc
)
SELECT procedure_code,
       procedure_description,
       COUNT(*) AS n_procedures,
       SUM(has_followup_14d) AS n_with_followup_14d,
       ROUND(100 * SUM(has_followup_14d) / NULLIF(COUNT(*), 0), 2) AS pct_with_followup_14d
FROM proc_flags
GROUP BY procedure_code, procedure_description;

SELECT * FROM rpt_followup_14d_by_proc_code
ORDER BY pct_with_followup_14d ASC, n_procedures DESC
LIMIT 25;
