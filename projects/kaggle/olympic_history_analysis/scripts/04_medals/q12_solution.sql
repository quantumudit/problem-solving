-- Which are the top 5 countries by total medals won?

WITH medals_per_country AS (
    SELECT
        nr.region AS country,
        COUNT(ae.Medal) AS total_medals,
        DENSE_RANK() OVER (ORDER BY COUNT(ae.Medal) DESC) AS rnk
    FROM athlete_events AS ae
    JOIN noc_regions AS nr USING (NOC)
    WHERE ae.Medal != 'NA'
    GROUP BY nr.region
)

SELECT
    country,
    total_medals,
    rnk AS country_rank
FROM medals_per_country
WHERE rnk <= 5
ORDER BY rnk;
