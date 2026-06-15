import random
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from templates import TEMPLATES, fill_madlib, get_placeholders

app = typer.Typer()
console = Console()


def _article(word: str) -> str:
    return "an" if word[0].lower() in "aeiou" else "a"


@app.command()
def play(
    story: str | None = typer.Option(None, "--story", "-s", help="Story name to play"),
) -> None:
    if story is None:
        story = random.choice(list(TEMPLATES.keys()))
        console.print(f"[dim]No story selected -- picked '[bold]{story}[/bold]' at random.[/dim]")
    elif story not in TEMPLATES:
        console.print(f"[red]Unknown story '{story}'. Run 'list' to see available stories.[/red]")
        raise typer.Exit(code=1)

    template = TEMPLATES[story]
    placeholders = get_placeholders(template)

    console.print(Panel(
        f"Placeholders : {', '.join(placeholders)}",
        title=f"Mad Libs -- {story}",
        border_style="cyan",
    ))

    words: dict[str, str] = {}
    for placeholder in placeholders:
        while True:
            value = typer.prompt(f"Enter {_article(placeholder)} {placeholder}").strip()
            if value:
                words[placeholder] = value
                break
            console.print("[red]Value cannot be empty -- try again.[/red]")

    # wrap each filled word in bold cyan so it stands out in the final story
    highlighted_words = {k: f"[bold cyan]{v}[/bold cyan]" for k, v in words.items()}
    console.print(Panel(
        fill_madlib(template, highlighted_words),
        title=story.capitalize(),
        border_style="green",
    ))


@app.command(name="list")
def list_stories() -> None:
    table = Table(title="Available Stories", show_lines=True)
    table.add_column("Story", style="bold")
    table.add_column("Placeholders")
    for name, template in TEMPLATES.items():
        table.add_row(name, ", ".join(get_placeholders(template)))
    console.print(table)


if __name__ == "__main__":
    app()
