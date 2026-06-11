import polars as pl

result = (
    facebook_web_log
    .with_columns(date=pl.col("timestamp").dt.date())
    .group_by("user_id", "date")
    .agg(
        pl.col("timestamp")
        .filter(pl.col("action") == "page_load")
        .max()
        .alias("load_time"),
        pl.col("timestamp")
        .filter(pl.col("action") == "page_exit")
        .min()
        .alias("exit_time"),
    )
    .filter(pl.col("exit_time") > pl.col("load_time"))
    .with_columns(duration=pl.col("exit_time") - pl.col("load_time"))
    .group_by("user_id")
    .agg(pl.col("duration").mean())
)
