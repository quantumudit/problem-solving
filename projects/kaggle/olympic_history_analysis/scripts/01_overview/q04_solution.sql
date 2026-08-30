-- Which Olympic Game had the highest and lowest number of participating nations?

WITH cte AS
(
    SELECT
        Games,
        COUNT(DISTINCT nr.region) AS nations_participated
    FROM athlete_events
    JOIN noc_regions AS nr USING (NOC)
    GROUP BY Games
)

SELECT Games, nations_participated, 'Highest' AS category
FROM cte
WHERE nations_participated = (SELECT MAX(nations_participated) FROM cte)

UNION ALL

SELECT Games, nations_participated, 'Lowest' AS category
FROM cte
WHERE nations_participated = (SELECT MIN(nations_participated) FROM cte)

ORDER BY nations_participated DESC;
