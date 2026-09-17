import re
from pathlib import Path

import pandas as pd

data_dir = Path(__file__).parent / "data"

sql = (data_dir / "storedb.sql").read_text()

pattern = (
    r"insert into store_sales values"
    r" \('([^']+)',\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\);"
)

rows = [
    {
        "sale_date": m.group(1),
        "day_of_year": int(m.group(2)),
        "employee_shifts": int(m.group(3)),
        "units_sold": int(m.group(4)),
        "revenue": int(m.group(5)),
        "month_of_year": int(m.group(6)),
    }
    for m in re.finditer(pattern, sql)
]

df = pd.DataFrame(rows)
df["sale_date"] = pd.to_datetime(df["sale_date"], format="%d-%b-%Y").dt.strftime("%Y-%m-%d")
df.to_csv(data_dir / "store_sales.csv", index=False)

print(f"Exported {len(df)} rows to store_sales.csv")
