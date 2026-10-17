from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "movie_ratings_data.csv")

# -- q07: KDE -- Budget vs RT Ratings and Budget vs Audience Ratings --
# Plot two side-by-side bivariate KDE plots (1 row, 2 columns):
#   Left:  Budget (Mn $) vs Rotten Tomatoes Ratings %
#   Right: Budget (Mn $) vs Audience Ratings %
# Use a dark background style and share the x-axis across both plots.
