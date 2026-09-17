from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "basketball_players_data.csv", index_col="RowID")

# -- q02: Salary per Game and Salary per Field Goal Trend --
# Derive two new metrics by dividing Salary by Games Played and Salary by Field Goals.
# Plot each as a separate line chart comparing all players over the years.
