-- Users By Average Session Time --

WITH page_load_log AS
(
    SELECT
        user_id,
        timestamp::DATE AS date,
        MAX(timestamp) AS load_time
    FROM
        facebook_web_log
    WHERE
        action = 'page_load'
    GROUP BY
        user_id, timestamp::DATE
),

page_exit_log AS
(
    SELECT
        user_id,
        timestamp::DATE AS date,
        MIN(timestamp) AS exit_time
    FROM
        facebook_web_log
    WHERE
        action = 'page_exit'
    GROUP BY
        user_id, timestamp::DATE
)


SELECT
    pl.user_id,
    AVG(pe.exit_time - pl.load_time) AS duration
FROM
    page_load_log AS pl
    INNER JOIN page_exit_log AS pe
    ON pl.user_id = pe.user_id
    AND pl.date = pe.date
    AND pl.load_time < pe.exit_time
GROUP BY
    pl.user_id;
