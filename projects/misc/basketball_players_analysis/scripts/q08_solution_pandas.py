from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q08: Points per Field Goal Trend --
# Derive a metric: Points / Field Goals.
# Plot a line chart comparing all players over the years to analyze scoring style.
