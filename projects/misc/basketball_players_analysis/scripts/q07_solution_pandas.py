from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q07: Minutes per Game and Field Goals per Minute Trend --
# Derive two metrics: Minutes Played / Games Played and Field Goals / Minutes Played.
# Plot each as a separate line chart comparing all players over the years.
