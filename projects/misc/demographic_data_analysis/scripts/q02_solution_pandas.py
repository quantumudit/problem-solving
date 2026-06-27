from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "demographic_data.csv")

top_10_by_internet_users = df.nlargest(10, "Internet Users")[
    ["Country Name", "Internet Users"]
]
bottom_10_by_internet_users = df.nsmallest(10, "Internet Users")[
    ["Country Name", "Internet Users"]
]

show(top_10_by_internet_users, "Top 10 Countries by Internet Users")
show(bottom_10_by_internet_users, "Bottom 10 Countries by Internet Users")
