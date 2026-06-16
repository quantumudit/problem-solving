import typer
from rich.console import Console

from utils import Circle

app = typer.Typer()
console = Console()


@app.command()
def demo(
    radius: float = typer.Argument(..., help="Radius of the circle"),
) -> None:
    try:
        circle = Circle(radius)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)
    circle.display()


if __name__ == "__main__":
    app()
