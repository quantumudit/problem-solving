import math
import random

# -------------------------------------------------------
# Constants
# -------------------------------------------------------

CHOICES = ("rock", "paper", "scissors")
DEFAULT_ROUNDS = 3

# frozenset created once at module level -- not rebuilt on every call
_WINNING_PAIRS = frozenset({
    ("rock", "scissors"),
    ("scissors", "paper"),
    ("paper", "rock"),
})

# -------------------------------------------------------
# Core Logic
# -------------------------------------------------------

def validate_rounds(n: int) -> None:
    if n < 1 or n > 9 or n % 2 == 0:
        raise ValueError("Rounds must be an odd number between 1 and 9.")


def win_threshold(n: int) -> int:
    return math.ceil(n / 2)


def get_computer_move() -> str:
    return random.choice(CHOICES)


def determine_winner(human: str, robot: str) -> str:
    if human == robot:
        return "tie"
    return "human" if (human, robot) in _WINNING_PAIRS else "robot"
