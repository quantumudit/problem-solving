from pathlib import Path

import pandas as pd

from utils import show

data_dir = Path(__file__).parent.parent / "data"

df = pd.read_csv(data_dir / "movie_ratings_data.csv")

# -- q01: Top-10 Movies by Budget, RT Ratings, and Audience Ratings --
# Use nlargest() to get the top-10 movies for each metric separately.
# Display each result as a table using show().
