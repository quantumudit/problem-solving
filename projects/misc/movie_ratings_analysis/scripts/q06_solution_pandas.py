from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "movie_ratings_data.csv")

# -- q06: KDE -- RT Ratings vs Audience Ratings --
# Plot a bivariate KDE plot with Rotten Tomatoes Ratings % on the x-axis
# and Audience Ratings % on the y-axis to show where movies are most concentrated.
# Use a dark background style for contrast.
