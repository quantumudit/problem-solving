-- Which nations have participated in every Olympic Game?

SELECT
    nr.region,
    COUNT(DISTINCT ae.Games) AS games_participated
FROM athlete_events AS ae
JOIN noc_regions AS nr USING (NOC)
GROUP BY nr.region
HAVING COUNT(DISTINCT ae.Games) = (SELECT COUNT(DISTINCT Games) FROM athlete_events)
ORDER BY nr.region;
