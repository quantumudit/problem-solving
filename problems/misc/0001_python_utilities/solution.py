import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from utils import (
    fizzbuzz as fizzbuzz_sequence,
    minutes_to_seconds,
    sign_and_parity,
    sum_two_numbers,
)

app = typer.Typer(help="A small toolkit of Python utility functions.")
console = Console()


def _error(message: str) -> None:
    console.print(Panel(f"[red]{message}[/red]", title="Error", border_style="red", expand=False))
    raise typer.Exit(code=1)


@app.command()
def convert(
    minutes: int = typer.Argument(..., help="Number of minutes to convert to seconds"),
):
    """Convert minutes to seconds."""
    try:
        result = minutes_to_seconds(minutes)
    except ValueError as e:
        _error(str(e))

    console.print(Panel(
        f"[bold]{minutes}[/bold] minutes = [green bold]{result}[/green bold] seconds",
        title="Unit Converter",
        border_style="cyan",
        expand=False,
    ))


@app.command()
def add(
    num1: float = typer.Argument(..., help="First number"),
    num2: float = typer.Argument(..., help="Second number"),
):
    """Add two numbers together."""
    try:
        result = sum_two_numbers(num1, num2)
    except ValueError as e:
        _error(str(e))

    console.print(Panel(
        f"[bold]{num1:g} + {num2:g}[/bold] = [green bold]{result:g}[/green bold]",
        title="Sum",
        border_style="cyan",
        expand=False,
    ))


@app.command()
def fizzbuzz(
    n: int = typer.Argument(..., help="Upper bound of the sequence (inclusive)"),
):
    """Print the FizzBuzz sequence from 1 to N."""
    try:
        sequence = fizzbuzz_sequence(n)
    except ValueError as e:
        _error(str(e))

    table = Table(title=f"FizzBuzz (1 to {n})")
    table.add_column("n", justify="right", style="dim", min_width=4)
    table.add_column("Result", min_width=8)

    for i, value in enumerate(sequence, start=1):
        if value == "FizzBuzz":
            styled = f"[magenta bold]{value}[/magenta bold]"
        elif value == "Fizz":
            styled = f"[green]{value}[/green]"
        elif value == "Buzz":
            styled = f"[yellow]{value}[/yellow]"
        else:
            styled = value
        table.add_row(str(i), styled)

    console.print(table)


@app.command()
def parity(
    num: int = typer.Argument(..., help="Integer to inspect (for negatives use: parity -- -4)"),
):
    """Check the sign and parity of an integer."""
    try:
        sign, par = sign_and_parity(num)
    except ValueError as e:
        _error(str(e))

    sign_color = "green" if sign == "Positive" else "red" if sign == "Negative" else "yellow"

    console.print(Panel(
        f"[bold]Number:[/bold] {num}\n"
        f"[bold]Sign:  [/bold] [{sign_color}]{sign}[/{sign_color}]\n"
        f"[bold]Parity:[/bold] [cyan]{par}[/cyan]",
        title="Sign & Parity",
        border_style="cyan",
        expand=False,
    ))


if __name__ == "__main__":
    app()
