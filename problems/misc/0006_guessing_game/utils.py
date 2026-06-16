import random

DIFFICULTY_RANGES = {
    "easy": (1, 50),
    "medium": (1, 100),
    "hard": (1, 500),
}

MAX_ATTEMPTS = 10
HARD_ATTEMPTS = 7


def guessing_game(difficulty: str) -> int:
    normalized = difficulty.lower()
    if normalized not in DIFFICULTY_RANGES:
        raise ValueError("Valid options are: easy/medium/hard")

    low, high = DIFFICULTY_RANGES[normalized]
    return random.randint(low, high)


def get_available_attempts(difficulty: str) -> int:
    return HARD_ATTEMPTS if difficulty.lower() == "hard" else MAX_ATTEMPTS


def prompt_guess() -> int:
    while True:
        try:
            return int(input("Guess the number: "))
        except ValueError:
            print("Please enter a valid integer.")


def play_guessing_game(difficulty: str) -> None:
    difficulty = difficulty.lower()
    secret_number = guessing_game(difficulty)
    max_attempts = get_available_attempts(difficulty)
    attempts = 0

    while True:
        if difficulty != "easy" and attempts >= max_attempts:
            print(
                f"You have exhausted all the {attempts} attempts. The correct number is "
                f"{secret_number}"
            )
            break

        guess = prompt_guess()
        attempts += 1

        if guess > secret_number:
            print("Too High")
        elif guess < secret_number:
            print("Too Low")
        else:
            print(f"Congratulations! You got it in {attempts} attempts")
            break


if __name__ == "__main__":
    play_guessing_game("easy")
        