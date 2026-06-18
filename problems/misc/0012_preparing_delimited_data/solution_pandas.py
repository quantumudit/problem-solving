from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent / "data"

# Each row is a single comma-delimited string:
# "Mary had a little lamb...",123,'16-JUN-01'
poems = pd.read_csv(data_dir / "poems.csv")

# Split once into three positional columns
parts = poems["Field_1"].str.split(",", expand=True)

cleaned = pd.DataFrame({
    "poem": parts[0].str.strip().str.strip('"'),
    "poem_id": parts[1].str.strip().astype(int),
    "poem_read_date": pd.to_datetime(
        parts[2].str.strip().str.strip("'"), format="%d-%b-%y"
    ).dt.date,
})

show(cleaned)
