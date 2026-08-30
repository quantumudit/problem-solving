-- Who are the top-3 oldest athletes to win a Gold medal?

WITH gold_medal_athletes AS (
    SELECT
        Name,
        TRY_CAST(Age AS INTEGER) AS age,
        DENSE_RANK() OVER (ORDER BY TRY_CAST(Age AS INTEGER) DESC) AS rnk
    FROM athlete_events
    WHERE Medal = 'Gold'
        AND Age != 'NA'
)

SELECT Name, age, rnk
FROM gold_medal_athletes
WHERE rnk <= 3
ORDER BY rnk;
