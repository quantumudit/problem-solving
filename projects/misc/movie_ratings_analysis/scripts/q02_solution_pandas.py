from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "movie_ratings_data.csv")

# -- q02: Budget Distribution by Genre --
# Plot 3 separate histograms:
#   1. Budget distribution for Drama genre only
#   2. Budget distribution comparing Drama vs Action genre (overlapping)
#   3. Budget distribution stacked by all genres
