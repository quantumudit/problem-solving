from pathlib import Path

import duckdb
import typer

from utils import show

app = typer.Typer()

scripts_dir = Path(__file__).parent
data_dir = scripts_dir.parent / "data"


@app.command()
def run(
    q: str = typer.Argument(..., help="Question prefix, e.g. q01"),
    version: str = typer.Argument("", help="Optional version suffix, e.g. v2, v3"),
) -> None:
    suffix = f"_{version}" if version else ""
    sql_file = next(scripts_dir.rglob(f"{q}_solution{suffix}.sql"))

    athlete_events_path = (data_dir / "athlete_events.csv").as_posix()
    noc_regions_path = (data_dir / "noc_regions.csv").as_posix()

    conn = duckdb.connect()
    conn.execute(
        f"CREATE VIEW athlete_events AS SELECT * FROM read_csv_auto('{athlete_events_path}')"
    )
    conn.execute(
        f"CREATE VIEW noc_regions AS SELECT * FROM read_csv_auto('{noc_regions_path}')"
    )

    sql = sql_file.read_text()
    result = conn.execute(sql).df()
    show(result, q)


if __name__ == "__main__":
    app()
