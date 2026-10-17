from pathlib import Path

import pandas as pd
import yaml

data_dir = Path(__file__).parent / "data"

with open(data_dir / "basketball_players.yaml") as f:
    raw = yaml.safe_load(f)

years = raw["years"]
records = [
    {"Player": player, "Measure": measure, "Year": year, "Values": val}
    for player, metrics in raw["players"].items()
    for measure, values in metrics.items()
    for year, val in zip(years, values)
]

df = pd.DataFrame(records)
df.index.name = "RowID"
df.to_csv(data_dir / "basketball_players_data.csv")

print(f"Exported {len(df)} rows to basketball_players_data.csv")
