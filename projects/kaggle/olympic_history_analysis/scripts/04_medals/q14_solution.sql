-- Which countries have won Silver or Bronze medals but never won Gold?

WITH medal_counts AS (
    SELECT
        nr.region AS country,
        COUNT(CASE WHEN ae.Medal = 'Gold'   THEN 1 END) AS gold,
        COUNT(CASE WHEN ae.Medal = 'Silver' THEN 1 END) AS silver,
        COUNT(CASE WHEN ae.Medal = 'Bronze' THEN 1 END) AS bronze
    FROM athlete_events AS ae
    JOIN noc_regions AS nr USING (NOC)
    GROUP BY nr.region
)

SELECT
    country,
    silver,
    bronze
FROM medal_counts
WHERE gold = 0
    AND (silver > 0 OR bronze > 0)
ORDER BY silver DESC, bronze DESC;
