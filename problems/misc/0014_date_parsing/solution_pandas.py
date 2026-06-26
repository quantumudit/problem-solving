from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent / "data"

raw_df = pd.read_csv(data_dir / "date_embedded_text.csv")

text_df = raw_df.rename(columns={"Field_1": "Text"})

# matches DD-MON-YY(YY) and Mon DD[,] YYYY date formats
pattern = r"(\d{1,2}-\w{3,4}-\d{2,4}|\w{3}\s\d{1,2},?\s\d{4})"

text_df["date_str"] = text_df["Text"].str.extract(pattern)
text_df["parsed_date"] = pd.to_datetime(text_df["date_str"], format="mixed", errors="coerce")

# 2-digit years (e.g. "00") can parse as 2100 instead of 2000 -- roll back a century
current_year = pd.Timestamp.now().year
future_mask = text_df["parsed_date"].dt.year > current_year
text_df.loc[future_mask, "parsed_date"] -= pd.DateOffset(years=100)

result_df = text_df[["Text", "parsed_date"]].rename(columns={"parsed_date": "Date"})

show(result_df, "Date Parsing")
