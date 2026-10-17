from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q06: Field Goal Attempts per Game and Points per Game Trend --
# Derive two metrics: Field Goal Attempts / Games Played and Points / Games Played.
# Plot each as a separate line chart comparing all players over the years.
