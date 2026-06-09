"""
Rich-based display utilities for pandas, polars, and PySpark DataFrames.

Functions
---------
show(data, title, max_rows)  -- pretty-print a DataFrame as a Rich table
peek(data, n, title)         -- display the first n rows
info(data)                   -- print row count, column count, and column names
shape(data)                  -- print the (rows, columns) shape
columns(data)                -- print a formatted list of column names
nulls(data)                  -- display null counts per column as a table
"""

from typing import Any

import pandas as pd
import polars as pl
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def _to_pandas(data: Any) -> pd.DataFrame:
    """Convert a pandas, polars, or PySpark DataFrame to a pandas DataFrame."""
    if isinstance(data, pl.DataFrame):
        return data.to_pandas()

    if isinstance(data, pd.DataFrame):
        return data

    if hasattr(data, "toPandas"):
        return data.toPandas()

    raise TypeError(f"Unsupported dataframe type: {type(data)}")


def show(
    data: Any,
    title: str = "Results",
    max_rows: int | None = None,
) -> None:
    """Pretty-print a DataFrame as a Rich table.

    Parameters
    ----------
    data : DataFrame
        Accepts pandas, polars, or PySpark DataFrames.
    title : str
        Table title displayed above the output.
    max_rows : int | None
        Cap the number of rows shown. None displays all rows.
    """
    df = _to_pandas(data)

    if max_rows is not None:
        df = df.head(max_rows)

    table = Table(title=title)

    for col in df.columns:
        table.add_column(str(col))

    for row in df.astype(str).values:
        table.add_row(*row)

    console.print(table)


def peek(
    data: Any,
    n: int = 5,
    title: str = "Preview",
) -> None:
    """Display the first n rows of a DataFrame."""
    show(
        data,
        title=title,
        max_rows=n,
    )


def info(data: Any) -> None:
    """Print row count, column count, and column names in a panel."""
    df = _to_pandas(data)

    console.print(
        Panel.fit(
            f"""
Rows    : {len(df):,}
Columns : {len(df.columns)}

Column Names:
{", ".join(df.columns)}
""".strip(),
            title="DataFrame Info",
        )
    )


def shape(data: Any) -> None:
    """Print the (rows, columns) shape of a DataFrame."""
    df = _to_pandas(data)

    console.print(f"[bold cyan]Shape:[/bold cyan] {df.shape}")


def columns(data: Any) -> None:
    """Print a formatted list of column names."""
    df = _to_pandas(data)

    console.print("[bold cyan]Columns:[/bold cyan]")

    for col in df.columns:
        console.print(f" - {col}")


def nulls(data: Any) -> None:
    """Display null counts per column as a Rich table."""
    df = _to_pandas(data)

    null_df = pd.DataFrame(
        {
            "Column": df.columns,
            "NullCount": df.isna().sum().values,
        }
    )

    show(
        null_df,
        title="Null Analysis",
    )
