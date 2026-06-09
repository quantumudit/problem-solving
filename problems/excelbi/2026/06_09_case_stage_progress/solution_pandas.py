from pathlib import Path

import pandas as pd

from utils import show

data_file = Path(__file__).parent / "data" / "cases.csv"
df = pd.read_csv(data_file)


def get_current_stage(g: pd.DataFrame) -> str:
    if g["Cleared"].any():
        return g.loc[g["Cleared"]].sort_values("StageNo")["StageName"].iloc[-1]
    return "Not Started"


def get_next_stage(g: pd.DataFrame) -> str:
    # If there are no uncleared stages, the process is complete.
    if not (~g["Cleared"]).any():
        return "Completed"

    # Find the current stage number. If no stages are cleared yet, return 0
    current_stage_no = g.loc[g["Cleared"], "StageNo"].max() if g["Cleared"].any() else 0

    # Keep only uncleared stages that come after the current stage.
    next_stages = g.loc[(~g["Cleared"]) & (g["StageNo"] > current_stage_no)]

    # If there are no remaining stages post the current stage, return completed.
    if next_stages.empty:
        return "Completed"

    # Return the stage name corresponding to the earliest uncleared stage.
    return next_stages.sort_values("StageNo")["StageName"].iloc[0]


def get_progress(g: pd.DataFrame) -> tuple[str, float]:
    progress_pct = round(g["Cleared"].mean() * 100, 2)

    if progress_pct == 0:
        return "Not Started", progress_pct

    if progress_pct == 100:
        return "Completed", progress_pct

    return "In Progress", progress_pct


def get_process_issue(g: pd.DataFrame) -> str:
    if not (g["Cleared"].any() and (~g["Cleared"]).any()):
        return "No"
    current_stage_no = g.loc[g["Cleared"], "StageNo"].max()
    next_stage_no = g.loc[~g["Cleared"], "StageNo"].min()

    return "Yes" if current_stage_no > next_stage_no else "No"


def summarize_case(g: pd.DataFrame) -> pd.Series:
    status, progress_pct = get_progress(g)

    return pd.Series(
        {
            "CurrentStage": get_current_stage(g),
            "NextStage": get_next_stage(g),
            "Status": status,
            "ProcessIssue": get_process_issue(g),
            "ProgressPct": f"{progress_pct:.0f}%",
        }
    )


result = df.groupby("CaseID").apply(summarize_case).reset_index()

show(result, "Case Summary")
