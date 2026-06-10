from pathlib import Path

import pandas as pd

from utils import show

MONTH_TO_NUMBER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def territory_acquisition(revenue_df: pd.DataFrame) -> pd.DataFrame:
    df = revenue_df.copy()
    df["MonthNo"] = df["Month"].map(MONTH_TO_NUMBER)
    df = df.sort_values("MonthNo")

    # Each territory starts as its own owner; map is updated as acquisitions happen
    owner_map: dict[str, str] = {t: t for t in df["Territory"].unique()}

    for month_number, monthly_df in df.groupby("MonthNo"):
        monthly_df = monthly_df.copy()
        # Resolve current ownership before aggregating -- territories may have changed hands
        monthly_df["Owner"] = monthly_df["Territory"].map(owner_map)

        owner_revenue = monthly_df.groupby("Owner")["Revenue"].sum()
        top = owner_revenue.idxmax()
        bottom = owner_revenue.idxmin()

        print(f"Month {month_number}: {top} acquires {bottom}")

        # top == bottom means all territories belong to one owner -- consolidation complete
        if top == bottom:
            print()
            break

        # Transfer every territory belonging to the lowest-revenue owner to the top owner
        for territory, owner in owner_map.items():
            if owner == bottom:
                owner_map[territory] = top

    # Collapse territory list per owner into a comma-separated string
    return (
        pd.DataFrame({"Territory": owner_map.keys(), "Owner": owner_map.values()})
        .groupby("Owner")["Territory"]
        .apply(lambda ts: ", ".join(sorted(ts)))
        .reset_index()
    )


DATA_FILE = Path(__file__).parent / "data" / "revenues.csv"
revenue_df = pd.read_csv(DATA_FILE).dropna()

show(territory_acquisition(revenue_df), "Final Ownership Structure")
