from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent / "data"

raw_df = pd.read_csv(data_dir / "womens_clothing_ecom_reviews.csv")

filtered_df = raw_df[raw_df["Positive Feedback Count"] >= 10]

avg_ratings_df = (
    filtered_df.groupby(["Class Name", "Clothing ID"])["Rating"].mean().round(2).reset_index()
)

# dense rank: ties share a rank with no gaps (1, 2, 2, 3 not 1, 2, 2, 4)
avg_ratings_df["Rating Rank"] = (
    avg_ratings_df.groupby("Class Name")["Rating"]
    .rank(ascending=False, method="dense")
    .astype(int)
)

result_df = (
    avg_ratings_df[avg_ratings_df["Rating Rank"] <= 5]
    .sort_values(by=["Class Name", "Rating Rank", "Clothing ID"], ascending=True)
    .reset_index(drop=True)
)

show(result_df, "Top 5 Rated Items per Class", 15)
