from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "demographic_data.csv")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=df, x="Income Group", y="Birth Rate", ax=axes[0])
axes[0].set_title("Birth Rate by Income Group")
axes[0].tick_params(axis="x", rotation=15)

sns.boxplot(data=df, x="Income Group", y="Internet Users", ax=axes[1])
axes[1].set_title("Internet Users by Income Group")
axes[1].tick_params(axis="x", rotation=15)

plt.tight_layout()
plt.savefig(output_dir / "q05_boxplots_by_income_group.png", dpi=150)
plt.show()
