from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q03: Games Played Trend -- All Players --
# Plot a line chart showing the number of games played by each player from 2005 to 2014.
# Highlight any sharp drops caused by injuries (e.g. Kobe Bryant and Derrick Rose).
