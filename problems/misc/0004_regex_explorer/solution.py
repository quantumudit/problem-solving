import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from utils import TextAnalysis

app = typer.Typer()
console = Console()


def _error(message: str) -> None:
    console.print(Panel(f"[red]{message}[/red]", title="Error", border_style="red", expand=False))
    raise typer.Exit(code=1)


def _highlight(text: str, matches: list[tuple[str, int]]) -> str:
    matched_positions = {pos for _, pos in matches}
    parts = []
    for i, char in enumerate(text):
        if i in matched_positions:
            parts.append(f"[bold red]{char}[/bold red]")
        else:
            parts.append(char)
    return "".join(parts)


def _context(text: str, pos: int, window: int = 3) -> str:
    start = max(0, pos - window)
    end = min(len(text), pos + window + 1)
    rel = pos - start
    excerpt = text[start:end]
    return excerpt[:rel] + f"[bold red]{excerpt[rel]}[/bold red]" + excerpt[rel + 1:]


@app.command()
def search(
    text: str = typer.Argument(..., help="Text to search for special characters"),
) -> None:
    if not text.strip():
        _error("Text cannot be empty.")

    ta = TextAnalysis(text=text)
    matches = ta.special_chars_pos()
    counts = ta.char_counts()

    console.print(Panel(
        _highlight(text, matches),
        title="Input Text",
        border_style="cyan",
    ))

    if matches:
        match_table = Table(title="Special Character Matches", show_lines=True)
        match_table.add_column("Match", justify="center", style="bold red")
        match_table.add_column("Index", justify="right")
        match_table.add_column("Context")
        for char, pos in matches:
            match_table.add_row(char, str(pos), _context(text, pos))
        console.print(match_table)
    else:
        console.print("[green]No special characters found.[/green]")

    counts_table = Table(title="Character Counts", show_lines=True)
    counts_table.add_column("Category", style="bold")
    counts_table.add_column("Count", justify="right")
    labels = {
        "special_chars":     "Special Characters",
        "uppercase_letters": "Uppercase Letters",
        "lowercase_letters": "Lowercase Letters",
        "whitespaces":       "Whitespaces",
        "digits":            "Digits",
        "total":             "Total",
    }
    for key, label in labels.items():
        counts_table.add_row(label, str(counts[key]), style="bold cyan" if key == "total" else "")
    console.print(counts_table)


if __name__ == "__main__":
    app()
