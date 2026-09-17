from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q01: Salary Trend -- All Players --
# Plot a line chart showing each player's salary trend from 2005 to 2014.
# Each player should be a separate line with a distinct color and marker.
