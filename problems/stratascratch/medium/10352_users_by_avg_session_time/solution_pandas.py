import pandas as pd

df = facebook_web_log.copy()
df["date"] = df["timestamp"].dt.date

# 1. Get max load and min exit as MultiIndexed Series
loads = df[df["action"] == "page_load"].groupby(["user_id", "date"])["timestamp"].max()
exits = df[df["action"] == "page_exit"].groupby(["user_id", "date"])["timestamp"].min()

# 2. Subtract directly. Pandas automatically aligns indices (acts like an inner join!)
durations = exits - loads

# 3. Filter valid durations and calculate mean per user
valid_durations = durations[durations > pd.Timedelta(0)]
result = valid_durations.groupby("user_id").mean().reset_index()
