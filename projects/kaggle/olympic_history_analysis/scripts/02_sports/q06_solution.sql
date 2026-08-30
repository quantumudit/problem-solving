-- Which sports have featured in every Summer Olympics?

SELECT
    Sport,
    COUNT(DISTINCT Games) AS summer_games_appeared
FROM athlete_events
WHERE Season = 'Summer'
GROUP BY Sport
HAVING COUNT(DISTINCT Games) = (SELECT COUNT(DISTINCT Games) FROM athlete_events WHERE Season = 'Summer')
ORDER BY Sport;
