from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "demographic_data.csv")

top_10_by_birth_rate = df.nlargest(10, "Birth Rate")[["Country Name", "Birth Rate"]]
bottom_10_by_birth_rate = df.nsmallest(10, "Birth Rate")[["Country Name", "Birth Rate"]]

show(top_10_by_birth_rate, "Top 10 Countries by Birth Rate")
show(bottom_10_by_birth_rate, "Bottom 10 Countries by Birth Rate")
