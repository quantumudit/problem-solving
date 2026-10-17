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

    store_sales_path = (data_dir / "store_sales.csv").as_posix()

    conn = duckdb.connect()
    conn.execute(
        f"CREATE VIEW store_sales AS SELECT * FROM read_csv_auto('{store_sales_path}')"
    )

    sql = sql_file.read_text()
    result = conn.execute(sql).df()
    show(result, q)


if __name__ == "__main__":
    app()
