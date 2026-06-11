SELECT
    user_id,
    AVG(exit_time - load_time) AS duration
FROM (
    SELECT
        user_id,
        timestamp::DATE AS date,
        MAX(CASE WHEN action = 'page_load' THEN timestamp END) AS load_time,
        MIN(CASE WHEN action = 'page_exit' THEN timestamp END) AS exit_time
    FROM facebook_web_log
    GROUP BY user_id, timestamp::DATE
) AS subquery
WHERE exit_time > load_time
GROUP BY user_id;
