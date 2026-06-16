import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from utils import (
    count_chars,
    filter_students,
    get_ranked_sales,
)

app = typer.Typer(help="Data utility functions for exploring and filtering records.")
console = Console()

STUDENTS: list[dict] = [
    {"name": "Alice",   "age": 20},
    {"name": "Bob",     "age": 25},
    {"name": "Carol",   "age": 18},
    {"name": "David",   "age": 22},
    {"name": "Eve",     "age": 19},
    {"name": "Frank",   "age": 30},
    {"name": "Grace",   "age": 17},
]

TRANSACTIONS: list[dict] = [
    {"product": "Widget",       "sales": 300},
    {"product": "Gadget",       "sales": 450},
    {"product": "Widget",       "sales": 200},
    {"product": "Gadget",       "sales": 100},
    {"product": "Doohickey",    "sales": 620},
    {"product": "Doohickey",    "sales": 80},
    {"product": "Thingamajig",  "sales": 390},
]


def _error(message: str) -> None:
    console.print(Panel(f"[red]{message}[/red]", title="Error", border_style="red", expand=False))
    raise typer.Exit(code=1)


@app.command()
def chars(
    text: str = typer.Option(
        ..., "--text", "-t",
        prompt="Enter text",
        help="Text to analyse",
    ),
    ignore_case: bool = typer.Option(
        True, "--ignore-case/--case-sensitive",
        help="Treat uppercase and lowercase as the same character",
    ),
):
    """Count the frequency of each character in a string."""
    try:
        freq = count_chars(text, ignore_case=ignore_case)
    except ValueError as e:
        _error(str(e))

    mode = "case-insensitive" if ignore_case else "case-sensitive"
    table = Table(title=f'Character Frequency ({mode})')
    table.add_column("Character", justify="center", min_width=12)
    table.add_column("Count", justify="right", min_width=6)

    for char, count in freq:
        table.add_row(repr(char), str(count))

    console.print(table)


@app.command()
def students(
    limit: int = typer.Option(
        21, "--limit", "-l",
        prompt="Age limit",
        help="Keep students strictly younger than this age",
    ),
):
    """Filter the sample student list by age."""
    filtered = filter_students(STUDENTS, age_limit=limit)

    if not filtered:
        console.print(Panel(
            f"[yellow]No students found under age {limit}.[/yellow]",
            title="Students",
            border_style="yellow",
            expand=False,
        ))
        return

    table = Table(title=f"Students Younger Than {limit}")
    table.add_column("Name", style="cyan", min_width=10)
    table.add_column("Age", justify="right", min_width=6)

    for student in filtered:
        table.add_row(student["name"], str(student["age"]))

    console.print(table)
    console.print(f"[dim]{len(filtered)} of {len(STUDENTS)} students match the filter.[/dim]")


@app.command()
def top_product():
    """Find the product with the highest total sales."""
    ranked = get_ranked_sales(TRANSACTIONS)
    winner, winner_total = ranked[0]

    table = Table(title="Sales by Product")
    table.add_column("Rank", justify="right", style="dim", min_width=4)
    table.add_column("Product", min_width=14)
    table.add_column("Total Sales", justify="right", min_width=12)

    for rank, (product, total) in enumerate(ranked, start=1):
        is_winner = product == winner
        product_cell = f"[bold green]{product}[/bold green]" if is_winner else product
        sales_cell = f"[bold green]${total:,.0f}[/bold green]" if is_winner else f"${total:,.0f}"
        table.add_row(str(rank), product_cell, sales_cell)

    console.print(table)
    console.print(Panel(
        f"[bold green]Top Product:[/bold green] {winner}  --  "
        f"[bold]Total Sales:[/bold] [green]${winner_total:,.0f}[/green]",
        title="Winner",
        border_style="green",
        expand=False,
    ))


if __name__ == "__main__":
    app()
