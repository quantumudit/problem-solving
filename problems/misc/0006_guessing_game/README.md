---
platform: misc
problem_id: "0006"
slug: guessing_game
difficulty: null
link: ""
dataset: none
---

# Guessing Game

A number-guessing game where the player tries to identify a randomly
chosen integer within a range determined by the selected difficulty.
The game gives directional hints after each wrong guess and enforces
an attempt limit on harder difficulties.

## Game Rules

1. At the start of each game, the program picks a random integer in the
   range for the chosen difficulty (both ends inclusive).
2. The player submits guesses one at a time.
3. After each wrong guess, display one of:
   - "Too high -- guess lower."
   - "Too low -- guess higher."
4. On a correct guess, display the number of attempts taken and a
   congratulations message.
5. Typing "quit" at any guess prompt exits immediately without revealing
   the answer.
6. On medium and hard, if the player exhausts all allowed attempts
   without guessing correctly, display the target number and a loss message.

## Difficulty Levels

| Difficulty | Range   | Max Attempts |
|------------|---------|--------------|
| easy       | 1 - 50  | unlimited    |
| medium     | 1 - 100 | 10           |
| hard       | 1 - 500 | 7            |

## CLI Interface

```
python solution.py play [--difficulty LEVEL]
```

- Default difficulty is `medium`.
- Valid values for `--difficulty`: `easy`, `medium`, `hard`.
- Typer handles argument parsing and prompts.

### Rich Output

- On startup, display a Rich panel showing the difficulty, the number
  range, and (for medium/hard) the attempt limit.
- After each guess, show the remaining attempts (where applicable) and
  the hint.
- At the end, display a styled result panel -- win or loss -- with the
  total attempts used.
