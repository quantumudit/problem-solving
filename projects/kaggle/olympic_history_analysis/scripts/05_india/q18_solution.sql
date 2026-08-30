-- In which Olympic Games did India win medals in Hockey, and how many?

SELECT
    ae.Games AS olympic_game,
    COUNT(ae.Medal) AS total_medals
FROM athlete_events AS ae
JOIN noc_regions AS nr USING (NOC)
WHERE ae.Medal != 'NA'
    AND nr.region = 'India'
    AND ae.Sport = 'Hockey'
GROUP BY ae.Games
ORDER BY ae.Games;
