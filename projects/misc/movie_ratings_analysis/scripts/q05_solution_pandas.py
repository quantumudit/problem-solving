from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "movie_ratings_data.csv")

# -- q05: RT vs Audience Ratings by Genre and Release Year --
# Plot a FacetGrid scatter plot with Genre as rows and Release Year as columns.
# Each cell shows RT Ratings % vs Audience Ratings % for that genre-year slice.
