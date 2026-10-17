from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q05: Field Goals per Game and Goal Accuracy Trend --
# Derive two metrics: Field Goals / Games Played and Field Goals / Field Goal Attempts.
# Plot each as a separate line chart comparing all players over the years.
