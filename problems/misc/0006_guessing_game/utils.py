import random

# -------------------------------------------------------
# Difficulty Config
# -------------------------------------------------------

DIFFICULTY_RANGES: dict[str, tuple[int, int]] = {
    "easy":   (1, 50),
    "medium": (1, 100),
    "hard":   (1, 500),
}

MAX_ATTEMPTS: dict[str, int | None] = {
    "easy":   None,  # unlimited
    "medium": 10,
    "hard":   7,
}

# -------------------------------------------------------
# Core Logic
# -------------------------------------------------------

def guessing_game(difficulty: str) -> int:
    if difficulty not in DIFFICULTY_RANGES:
        raise ValueError(f"Invalid difficulty '{difficulty}'. Choose: easy, medium, hard.")
    low, high = DIFFICULTY_RANGES[difficulty]
    return random.randint(low, high)


def get_available_attempts(difficulty: str) -> int | None:
    return MAX_ATTEMPTS[difficulty]


def check_guess(guess: int, secret: int) -> str:
    if guess > secret:
        return "high"
    if guess < secret:
        return "low"
    return "correct"
