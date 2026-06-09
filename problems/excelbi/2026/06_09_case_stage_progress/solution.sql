WITH stage_summary AS (
    SELECT
        CaseID,
        COALESCE(MAX(CASE WHEN Cleared THEN StageNo END), 0) AS CurrentStageNo,
        COALESCE(MIN(CASE WHEN NOT Cleared THEN StageNo END), MAX(StageNo)+1) AS FirstUnclearedStageNo,
        ROUND(AVG(CASE WHEN Cleared THEN 1.0 ELSE 0.0 END) * 100, 0) AS ProgressPct
    FROM
        cases
    GROUP BY
        CaseID
),

current_stage AS (
    SELECT
        s.CaseID,
        COALESCE(c.StageName, 'Not Started') AS CurrentStage
    FROM
        stage_summary AS s
        LEFT JOIN cases AS c
            ON s.CaseID = c.CaseID
            AND s.CurrentStageNo = c.StageNo
),

next_stage_candidates AS (
    SELECT
        c.CaseID,
        c.StageName,
        c.StageNo,
        ROW_NUMBER() OVER (PARTITION BY c.CaseID ORDER BY c.StageNo) AS rn
    FROM
        cases AS c
        INNER JOIN stage_summary AS s
            ON c.CaseID = s.CaseID
            AND c.Cleared = FALSE
            AND c.StageNo > COALESCE(s.CurrentStageNo, 0)
),

next_stage AS (
    SELECT
        CaseID,
        StageName AS NextStage
    FROM next_stage_candidates
    WHERE rn = 1
)

SELECT
    s.CaseID,
    cs.CurrentStage,
    COALESCE(ns.NextStage, 'Completed') AS NextStage,

    CASE
        WHEN s.ProgressPct = 0 THEN 'Not Started'
        WHEN s.ProgressPct = 100 THEN 'Completed'
        ELSE 'In Progress'
    END AS Status,

    CASE
        WHEN s.CurrentStageNo > s.FirstUnclearedStageNo THEN 'Yes'
        ELSE 'No'
    END AS ProcessIssue,
    CAST(s.ProgressPct AS INTEGER) || '%' AS ProgressPct
FROM
    stage_summary AS s
    LEFT JOIN current_stage AS cs
        ON s.CaseID = cs.CaseID
    LEFT JOIN next_stage AS ns
        ON s.CaseID = ns.CaseID
ORDER BY
    s.CaseID
