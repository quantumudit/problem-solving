from pathlib import Path

import polars as pl

from utils import show

data_file = Path(__file__).parent / "data" / "cases.csv"
df = pl.read_csv(data_file)

current_stage_expr = (
    pl.col("StageName")
    .sort_by("StageNo")
    .filter(pl.col("Cleared"))
    .last()
    .fill_null("Not Started")
    .alias("CurrentStage")
)

next_stage_expr = (
    pl.col("StageName")
    .sort_by("StageNo")
    .filter(
        (~pl.col("Cleared"))
        & (
            pl.col("StageNo")
            > pl.col("StageNo").filter(pl.col("Cleared")).max().fill_null(0)
        )
    )
    .first()
    .fill_null("Completed")
    .alias("NextStage")
)

progress_expr = (pl.col("Cleared").mean() * 100).cast(pl.Int64).alias("ProgressPct")

status_expr = (
    pl.when(progress_expr == 0)
    .then(pl.lit("Not Started"))
    .when(progress_expr == 100)
    .then(pl.lit("Completed"))
    .otherwise(pl.lit("In Progress"))
    .alias("Status")
)

process_issue_expr = (
    pl.when(
        pl.col("StageNo").filter(pl.col("Cleared")).max()
        > pl.col("StageNo").filter(~pl.col("Cleared")).min()
    )
    .then(pl.lit("Yes"))
    .otherwise(pl.lit("No"))
    .alias("ProcessIssue")
)

result = (
    df.group_by("CaseID")
    .agg(
        [
            current_stage_expr,
            next_stage_expr,
            status_expr,
            process_issue_expr,
            progress_expr,
        ]
    )
    .with_columns(pl.format("{}%", pl.col("ProgressPct")))
    .sort("CaseID")
)

show(result, "Case Summary")
