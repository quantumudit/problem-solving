from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_dir = Path(__file__).parent.parent / "data"
output_dir = Path(__file__).parent.parent / "output"

df = pd.read_csv(data_dir / "demographic_data.csv")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(df["Birth Rate"], bins=10, kde=True, ax=axes[0])
axes[0].set_title("Birth Rate Distribution")

sns.histplot(df["Internet Users"], bins=10, kde=True, ax=axes[1])
axes[1].set_title("Internet Users Distribution")

plt.tight_layout()
plt.savefig(output_dir / "q04_distributions.png", dpi=150)
plt.show()
