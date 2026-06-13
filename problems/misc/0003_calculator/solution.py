import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from utils import Calculator

app = typer.Typer()
console = Console()


def _parse_number(s: str) -> int | float:
    try:
        return int(s)
    except ValueError:
        return float(s)


def _show_history(calc: Calculator) -> None:
    entries = calc.get_history()
    if not entries:
        console.print("[yellow]No history yet.[/yellow]")
        return
    table = Table(title="History", show_lines=True)
    table.add_column("#", style="dim", justify="right")
    table.add_column("Computation")
    for i, entry in enumerate(entries, 1):
        table.add_row(str(i), entry)
    console.print(table)


def _handle_command(raw: str, calc: Calculator) -> bool:
    """Return True if input was a special command and was handled."""
    command = raw.lower()
    if command == "history":
        _show_history(calc)
        return True
    if command == "clear":
        calc.clear_history()
        console.print("[green]History cleared.[/green]")
        return True
    return False


@app.command()
def repl() -> None:
    while True:
        mode = (
            console.input("Mode ([bold]expression[/bold] / [bold]manual[/bold]): ")
            .strip()
            .lower()
        )
        if mode in ("expression", "manual"):
            break
        console.print("[red]Enter 'expression' or 'manual'.[/red]")

    calc = Calculator(mode=mode)  # type: ignore[arg-type]

    if mode == "expression":
        instructions = (
            "Operators : + - * / % ** ()\n"
            "Functions : sqrt()  abs()  round()\n"
            "Commands  : history | clear | exit | quit"
        )
    else:
        instructions = (
            "Enter two numbers and an operator when prompted.\n"
            "Operators : + - * / % **\n"
            "Commands  : history | clear | exit | quit  (at the First Number prompt)"
        )

    console.print(
        Panel(instructions, title=f"Calculator REPL [{mode}]", border_style="cyan")
    )

    while True:
        try:
            if mode == "expression":
                raw = console.input("[bold cyan]> [/bold cyan]").strip()
                if not raw:
                    continue
                if raw.lower() in ("exit", "quit"):
                    console.print("Bye!")
                    break
                if _handle_command(raw, calc):
                    continue
                result = calc.evaluate(raw)
                if result.startswith("Error"):
                    console.print(f"[red]{result}[/red]")
                else:
                    console.print(f"[green]{result}[/green]")

            else:
                a_raw = console.input(
                    "[bold cyan]  First Number     : [/bold cyan]"
                ).strip()
                if not a_raw:
                    continue
                if a_raw.lower() in ("exit", "quit"):
                    console.print("Bye!")
                    break
                if _handle_command(a_raw, calc):
                    continue
                try:
                    a = _parse_number(a_raw)
                except ValueError:
                    console.print(f"[red]Error: '{a_raw}' is not a valid number.[/red]")
                    continue

                b_raw = console.input(
                    "[bold cyan]  Second Number     : [/bold cyan]"
                ).strip()
                try:
                    b = _parse_number(b_raw)
                except ValueError:
                    console.print(f"[red]Error: '{b_raw}' is not a valid number.[/red]")
                    continue

                op = console.input("[bold cyan]  Operator : [/bold cyan]").strip()
                result = calc.compute(a, b, op)
                if result.startswith("Error"):
                    console.print(f"[red]{result}[/red]")
                else:
                    console.print(f"[green]{result}[/green]")

        except (EOFError, KeyboardInterrupt):
            console.print("\nBye!")
            break


if __name__ == "__main__":
    app()
