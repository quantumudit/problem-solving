-- Which Olympic Game had the highest and lowest number of participating nations?

WITH nations_per_game AS (
    SELECT
        Games,
        COUNT(DISTINCT nr.region) AS nations_participated
    FROM athlete_events
    JOIN noc_regions AS nr USING (NOC)
    GROUP BY Games
),

ranked_by_participation AS (
    SELECT
        Games,
        nations_participated,
        RANK() OVER (ORDER BY nations_participated ASC) AS rnk,
        'Lowest' AS category
    FROM nations_per_game

    UNION ALL

    SELECT
        Games,
        nations_participated,
        RANK() OVER (ORDER BY nations_participated DESC) AS rnk,
        'Highest' AS category
    FROM nations_per_game
)

SELECT
    Games,
    nations_participated,
    category
FROM ranked_by_participation
WHERE rnk = 1
ORDER BY nations_participated DESC;
