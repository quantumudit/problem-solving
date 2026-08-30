-- For each Olympic Game, which country won the most Gold, Silver, Bronze, and overall medals?

WITH medals_per_country_per_game AS (
    SELECT
        nr.region AS country,
        ae.Games AS olympic_game,
        COUNT(CASE WHEN ae.Medal = 'Gold'   THEN 1 END) AS gold,
        COUNT(CASE WHEN ae.Medal = 'Silver' THEN 1 END) AS silver,
        COUNT(CASE WHEN ae.Medal = 'Bronze' THEN 1 END) AS bronze,
        COUNT(CASE WHEN ae.Medal != 'NA'    THEN 1 END) AS total_medals
    FROM athlete_events AS ae
    JOIN noc_regions AS nr USING (NOC)
    GROUP BY nr.region, ae.Games
),

ranked_by_medal_type AS (
    SELECT
        country,
        olympic_game,
        RANK() OVER (PARTITION BY olympic_game ORDER BY gold DESC)         AS gold_rank,
        RANK() OVER (PARTITION BY olympic_game ORDER BY silver DESC)       AS silver_rank,
        RANK() OVER (PARTITION BY olympic_game ORDER BY bronze DESC)       AS bronze_rank,
        RANK() OVER (PARTITION BY olympic_game ORDER BY total_medals DESC) AS medals_rank
    FROM medals_per_country_per_game
)

SELECT
    olympic_game,
    MAX(CASE WHEN gold_rank = 1    THEN country END) AS most_gold_country,
    MAX(CASE WHEN silver_rank = 1  THEN country END) AS most_silver_country,
    MAX(CASE WHEN bronze_rank = 1  THEN country END) AS most_bronze_country,
    MAX(CASE WHEN medals_rank = 1  THEN country END) AS most_medals_country
FROM ranked_by_medal_type
GROUP BY olympic_game
ORDER BY olympic_game;
