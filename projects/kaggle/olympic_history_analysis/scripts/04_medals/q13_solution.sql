-- What is the total Gold, Silver, and Bronze medal count for each country?

SELECT
    nr.region AS country,
    COUNT(CASE WHEN ae.Medal = 'Gold'   THEN 1 END) AS gold,
    COUNT(CASE WHEN ae.Medal = 'Silver' THEN 1 END) AS silver,
    COUNT(CASE WHEN ae.Medal = 'Bronze' THEN 1 END) AS bronze
FROM athlete_events AS ae
JOIN noc_regions AS nr USING (NOC)
GROUP BY nr.region
ORDER BY gold DESC, silver DESC, bronze DESC;
