-- Which sport has won India the most medals?

WITH india_medals_by_sport AS (
    SELECT
        ae.Sport AS sport,
        COUNT(ae.Medal) AS total_medals,
        DENSE_RANK() OVER (ORDER BY COUNT(ae.Medal) DESC) AS rnk
    FROM athlete_events AS ae
    JOIN noc_regions AS nr USING (NOC)
    WHERE ae.Medal != 'NA'
        AND nr.region = 'India'
    GROUP BY ae.Sport
)

SELECT
    sport,
    total_medals
FROM india_medals_by_sport
WHERE rnk = 1;
