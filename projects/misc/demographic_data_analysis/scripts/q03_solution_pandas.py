from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "demographic_data.csv")

sns.scatterplot(
    data=df,
    x="Birth Rate",
    y="Internet Users",
    hue="Income Group",
    s=80,
)
plt.title("Birth Rate vs Internet Users by Income Group")
plt.tight_layout()
plt.savefig(output_dir / "q03_correlation.png", dpi=150)
plt.show()
