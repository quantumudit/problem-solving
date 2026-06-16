import typer
from rich.console import Console

from utils import DEFAULT_SALES, MONTHS, generate_sales_chart

app = typer.Typer()
console = Console()


def _prompt_sales() -> list[float]:
    console.print("[cyan]Enter sales value (in thousands USD) for each month:[/cyan]")
    sales_data = []
    for month in MONTHS:
        while True:
            raw = console.input(f"  [bold]{month}[/bold]: ").strip()
            try:
                sales_data.append(float(raw))
                break
            except ValueError:
                console.print("  [red]Please enter a valid number.[/red]")
    return sales_data


@app.command()
def chart(
    sales: bool = typer.Option(
        False, "--sales", "-s", help="Prompt for each month's sales value interactively"
    ),
) -> None:
    if sales:
        sales_data: list[int | float] = _prompt_sales()
    else:
        sales_data = DEFAULT_SALES
        console.print("[dim]No data provided -- using default sales figures.[/dim]")

    console.print(
        "[dim]"
        + "  ".join(f"{m}: {v:g}" for m, v in zip(MONTHS, sales_data))
        + "[/dim]"
    )

    generate_sales_chart(sales_data)
    console.print("[green]Chart saved to 'sales_trend.png'.[/green]")


if __name__ == "__main__":
    app()
