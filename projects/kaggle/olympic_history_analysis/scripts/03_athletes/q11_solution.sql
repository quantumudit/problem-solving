-- Who are the top 5 athletes with the most Gold medals?

WITH gold_medal_counts AS (
    SELECT
        Name,
        COUNT(Medal) AS total_gold_medals,
        DENSE_RANK() OVER (ORDER BY COUNT(Medal) DESC) AS rnk
    FROM athlete_events
    WHERE Medal = 'Gold'
    GROUP BY Name
)

SELECT
    Name,
    total_gold_medals,
    rnk AS gold_medals_rank
FROM gold_medal_counts
WHERE rnk <= 5
ORDER BY rnk;
