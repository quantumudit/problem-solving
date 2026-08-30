-- How many sports were played in each Olympic Game?

SELECT
    Games,
    COUNT(DISTINCT Sport) AS sports_played
FROM athlete_events
GROUP BY Games
ORDER BY Games;
