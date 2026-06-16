import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from utils import (
    CHOICES,
    DEFAULT_ROUNDS,
    determine_winner,
    get_computer_move,
    validate_rounds,
    win_threshold,
)

app = typer.Typer()
console = Console()

_RESULT_LABEL = {
    "human": ("Win",  "green"),
    "robot": ("Loss", "red"),
    "tie":   ("Draw", "yellow"),
}


@app.command()
def play(
    rounds: int = typer.Option(
        DEFAULT_ROUNDS, "--rounds", "-r", help="Number of rounds (odd, 1-9)"
    ),
) -> None:
    try:
        validate_rounds(rounds)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)

    threshold = win_threshold(rounds)
    console.print(Panel(
        f"Rounds    : {rounds}\n"
        f"Win needs : {threshold} wins",
        title="Rock Paper Scissors",
        border_style="cyan",
    ))

    human_wins = 0
    robot_wins = 0
    draws = 0
    rounds_played = 0
    history: list[tuple[int, str, str, str]] = []

    while rounds_played < rounds and human_wins < threshold and robot_wins < threshold:
        while True:
            raw = console.input("[bold]Your move (rock / paper / scissors): [/bold]").strip().lower()
            if raw in CHOICES:
                break
            console.print(f"[red]Invalid. Choose: {', '.join(CHOICES)}[/red]")

        computer = get_computer_move()
        result = determine_winner(raw, computer)
        rounds_played += 1

        if result == "human":
            human_wins += 1
        elif result == "robot":
            robot_wins += 1
        else:
            draws += 1

        label, color = _RESULT_LABEL[result]
        history.append((rounds_played, raw, computer, label))

        console.print(
            f"Round {rounds_played}: [bold]{raw}[/bold] vs [bold]{computer}[/bold] "
            f"-> [{color}]{label}[/{color}]   "
            f"You [green]{human_wins}[/green] | "
            f"Draw [yellow]{draws}[/yellow] | "
            f"CPU [red]{robot_wins}[/red]"
        )

    # match history table
    table = Table(title="Match History", show_lines=True)
    table.add_column("Round", justify="right", style="dim")
    table.add_column("You", justify="center")
    table.add_column("Computer", justify="center")
    table.add_column("Result", justify="center")
    for rnd, human_move, comp_move, label in history:
        label_color = {"Win": "green", "Loss": "red", "Draw": "yellow"}[label]
        table.add_row(str(rnd), human_move, comp_move, f"[{label_color}]{label}[/{label_color}]")
    console.print(table)

    # match summary panel
    if human_wins > robot_wins:
        summary, border = "[bold green]You win the match![/bold green]", "green"
    elif robot_wins > human_wins:
        summary, border = "[bold red]Computer wins the match![/bold red]", "red"
    else:
        summary, border = "[bold yellow]The match is a draw![/bold yellow]", "yellow"

    console.print(Panel(
        f"{summary}\n"
        f"[dim]You: {human_wins}  Draws: {draws}  Computer: {robot_wins}[/dim]",
        title="Match Over",
        border_style=border,
    ))


if __name__ == "__main__":
    app()
