from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "movie_ratings_data.csv")

# -- q03: Critic Ratings Distribution by Genre --
# Plot a violin plot showing the distribution of Rotten Tomatoes Ratings %
# across all genres. Each genre is one violin on the x-axis.
