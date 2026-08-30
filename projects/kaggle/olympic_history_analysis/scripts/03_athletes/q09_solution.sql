-- What is the ratio of male to female athletes across all Olympics?

SELECT
    ROUND(
        (SELECT COUNT(DISTINCT ID) FROM athlete_events WHERE Sex = 'M') * 1.0 /
        (SELECT COUNT(DISTINCT ID) FROM athlete_events WHERE Sex = 'F'),
        2
    ) AS male_to_female_ratio;
