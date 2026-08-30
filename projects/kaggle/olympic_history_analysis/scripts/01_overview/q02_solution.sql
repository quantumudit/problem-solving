-- List all Olympic Games held so far with their year, season, and host city

SELECT DISTINCT
    Games,
    Year,
    Season,
    City
FROM athlete_events
ORDER BY Year, Season;
