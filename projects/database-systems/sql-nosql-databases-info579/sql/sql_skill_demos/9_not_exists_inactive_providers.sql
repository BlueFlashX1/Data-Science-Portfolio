-- ============================================================
-- INFO 579 Final Project · Section 8.9: NOT EXISTS OPERATOR QUERY
-- Demonstrates: NOT EXISTS correlated subquery to find providers with no encounter records
-- Source: Matthew Thompson's final report PDF
-- ============================================================

-- Assignment prompt:
--   Write a query using the NOT EXISTS operator. Show the results and sort the results by
--   key field(s). Interpret the output.

CREATE TABLE rpt_inactive_providers_by_specialty AS
SELECT
  pr.provider_specialty,
  COUNT(*) AS n_inactive_providers
FROM provider pr
WHERE NOT EXISTS (
  SELECT 1
  FROM encounter e
  WHERE e.provider_id = pr.provider_id
    AND e.organization_id = pr.organization_id
)
GROUP BY pr.provider_specialty;

SELECT *
FROM rpt_inactive_providers_by_specialty
ORDER BY n_inactive_providers DESC, provider_specialty;
