-- Which sports were played only once in Olympic history?

SELECT
    Sport,
    COUNT(DISTINCT Games) AS games_appeared
FROM athlete_events
GROUP BY Sport
HAVING COUNT(DISTINCT Games) = 1
ORDER BY Sport;
