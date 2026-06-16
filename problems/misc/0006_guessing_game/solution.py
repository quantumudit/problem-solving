import typer
from rich.console import Console
from rich.panel import Panel

from utils import (
    DIFFICULTY_RANGES,
    check_guess,
    get_available_attempts,
    guessing_game,
)

app = typer.Typer()
console = Console()

_DIFFICULTY_COLOR = {
    "easy":   "green",
    "medium": "yellow",
    "hard":   "red",
}


@app.command()
def play(
    difficulty: str = typer.Option(
        "medium", "--difficulty", "-d", help="Difficulty: easy | medium | hard"
    ),
) -> None:
    difficulty = difficulty.strip().lower()

    if difficulty not in DIFFICULTY_RANGES:
        console.print(f"[red]Invalid difficulty '{difficulty}'. Choose: easy, medium, hard.[/red]")
        raise typer.Exit(code=1)

    secret = guessing_game(difficulty)
    max_att = get_available_attempts(difficulty)
    low, high = DIFFICULTY_RANGES[difficulty]
    color = _DIFFICULTY_COLOR[difficulty]

    attempts_line = (
        "Attempts  : Unlimited"
        if max_att is None
        else f"Attempts  : {max_att}"
    )
    console.print(Panel(
        f"Difficulty : [{color}]{difficulty.capitalize()}[/{color}]\n"
        f"Range      : {low} - {high}\n"
        f"{attempts_line}",
        title="Guessing Game",
        border_style=color,
    ))

    attempts = 0

    while True:
        if max_att is not None and attempts >= max_att:
            console.print(Panel(
                f"[red]Out of attempts. The number was [bold]{secret}[/bold].[/red]\n"
                f"[dim]Total attempts used: {attempts}[/dim]",
                title="Game Over",
                border_style="red",
            ))
            break

        raw = console.input("[bold]Guess: [/bold]").strip()

        if raw.lower() == "quit":
            console.print("[dim]Game exited. See you next time![/dim]")
            break

        try:
            guess = int(raw)
        except ValueError:
            console.print("[red]Please enter a valid integer.[/red]")
            continue

        attempts += 1
        result = check_guess(guess, secret)

        if result == "correct":
            noun = "attempt" if attempts == 1 else "attempts"
            console.print(Panel(
                f"[bold green]Correct! You guessed it in {attempts} {noun}.[/bold green]",
                title="You Win!",
                border_style="green",
            ))
            break

        if result == "high":
            console.print("[red]Too high -- guess lower.[/red]")
        else:
            console.print("[cyan]Too low -- guess higher.[/cyan]")

        if max_att is not None:
            console.print(f"[dim]Attempts remaining: {max_att - attempts}[/dim]")


if __name__ == "__main__":
    app()
