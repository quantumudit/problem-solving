best_paid_titles = (
    worker
    .merge(title, left_on="worker_id", right_on="worker_ref_id", how="inner")
    .loc[lambda df: df["salary"] == df["salary"].max(), ["worker_title"]]
    .rename(columns={"worker_title": "best_paid_title"})
    .drop_duplicates()
)
