-- What are the Gold, Silver, and Bronze medal counts for each country per Olympic Game?

SELECT
    nr.region AS country,
    ae.Games AS olympic_game,
    COUNT(CASE WHEN ae.Medal = 'Gold'   THEN 1 END) AS gold,
    COUNT(CASE WHEN ae.Medal = 'Silver' THEN 1 END) AS silver,
    COUNT(CASE WHEN ae.Medal = 'Bronze' THEN 1 END) AS bronze
FROM athlete_events AS ae
JOIN noc_regions AS nr USING (NOC)
GROUP BY nr.region, ae.Games
ORDER BY olympic_game, gold DESC, silver DESC, bronze DESC;
