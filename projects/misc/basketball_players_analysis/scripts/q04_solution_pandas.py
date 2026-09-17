from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q04: Minutes Played and Points Trend -- All Players --
# Plot two separate line charts: one for minutes played and one for total points,
# comparing all players from 2005 to 2014.
