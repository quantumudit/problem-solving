-- How many nations participated in each Olympic Game?
SELECT
    Games,
    COUNT(DISTINCT nr.region) AS nations_participated
FROM athlete_events
JOIN noc_regions AS nr USING (NOC)
GROUP BY Games
ORDER BY Games;
