import polars as pl

best_paid_titles = (
    worker.join(title, left_on="worker_id", right_on="worker_ref_id", how="inner")
    .filter(pl.col("salary") == pl.col("salary").max())
    .select(pl.col("worker_title").alias("best_paid_title"))
    .unique()
)
