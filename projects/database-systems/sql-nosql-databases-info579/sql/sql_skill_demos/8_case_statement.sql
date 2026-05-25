-- ============================================================
-- INFO 579 Final Project · Section 8.8: CASE STATEMENT QUERY
-- Demonstrates: CASE WHEN to categorize patients by healthcare coverage tier
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write a query using a CASE statement. Show the results and sort the results by key
--   field(s). Interpret the output.

SELECT patient_id,
       healthcare_coverage,
       CASE
         WHEN healthcare_coverage >= 10000 THEN 'High Coverage'
         WHEN healthcare_coverage >= 5000  THEN 'Medium Coverage'
         ELSE 'Low Coverage'
       END AS coverage_category
FROM patient
ORDER BY patient_id;

-- printed table of summed counts of each coverage
SELECT
  SUM(CASE WHEN healthcare_coverage >= 10000 THEN 1 ELSE 0 END) AS highcoverage_count,
  SUM(CASE WHEN healthcare_coverage >= 5000 AND healthcare_coverage < 10000 THEN 1 ELSE 0 END) AS mediumcoverage_count,
  SUM(CASE WHEN healthcare_coverage < 5000 THEN 1 ELSE 0 END) AS lowcoverage_count
FROM patient;
