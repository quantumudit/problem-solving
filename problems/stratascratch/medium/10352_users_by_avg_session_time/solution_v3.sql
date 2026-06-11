SELECT
    user_id,
    AVG(exit_time - load_time) AS duration
FROM (
    SELECT
        user_id,
        timestamp::DATE AS date,
        MAX(timestamp) FILTER (WHERE action = 'page_load') AS load_time,
        MIN(timestamp) FILTER (WHERE action = 'page_exit') AS exit_time
    FROM facebook_web_log
    GROUP BY user_id, date
) subquery
WHERE exit_time > load_time
GROUP BY user_id;
