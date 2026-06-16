import random
import math
from typing import Tuple

CHOICES = ("rock", "paper", "scissors")
DEFAULT_ROUNDS = 3


def prompt_user() -> str:
    while True:
        user_input = input("Pick between Rock/Paper/Scissors: ").strip().lower()
        if user_input in CHOICES:
            return user_input
        print(f"Invalid choice. Choose one of: {', '.join(CHOICES)}")


def determine_winner(human: str, robot: str) -> str:
    if human == robot:
        return "tie"
    winning_pairs = {
        ("rock", "scissors"),
        ("scissors", "paper"),
        ("paper", "rock"),
    }
    return "human" if (human, robot) in winning_pairs else "robot"


def play_game(total_rounds: int = DEFAULT_ROUNDS) -> None:
    # Validate: must be odd number between 1 and 9
    if total_rounds < 1 or total_rounds > 9 or total_rounds % 2 == 0:
        raise ValueError("total_rounds must be an odd number between 1 and 9")

    early_wins = math.ceil(total_rounds / 2)
    human_wins = 0
    robot_wins = 0
    rounds_played = 0

    while rounds_played < total_rounds and human_wins < early_wins and robot_wins < early_wins:
        human = prompt_user()
        robot = random.choice(CHOICES)
        result = determine_winner(human, robot)

        if result == "tie":
            print(f"Both picked {human}. It's a tie - replaying round.")
            continue

        rounds_played += 1
        if result == "human":
            human_wins += 1
            print(f"You won this round! Robot picked: {robot}")
        else:
            robot_wins += 1
            print(f"Robot won this round! Robot picked: {robot}")

        print(f"Score - You: {human_wins} Robot: {robot_wins} Rounds played: {rounds_played}/{total_rounds}")

    if human_wins > robot_wins:
        print("Human won")
    elif robot_wins > human_wins:
        print("Robot won")
    else:
        print("It's a draw")


if __name__ == "__main__":
    play_game()



