WITH RankedWorkers AS (
    SELECT
        t.worker_title,
        RANK() OVER (ORDER BY w.salary DESC) as salary_rank
    FROM worker w
    JOIN title t ON w.worker_id = t.worker_ref_id
)
SELECT DISTINCT worker_title AS best_paid_title
FROM RankedWorkers
WHERE salary_rank = 1;
