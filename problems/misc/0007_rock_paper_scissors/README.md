---
platform: misc
problem_id: "0007"
slug: rock_paper_scissors
difficulty: null
link: ""
dataset: none
---

# Rock Paper Scissors

A best-of-N rounds Rock Paper Scissors game against the computer.
The computer picks its move at random each round. Results are tracked
and displayed in a Rich scoreboard after each round, with a match
summary at the end.

## Game Rules

- Valid moves: rock, paper, scissors
- rock beats scissors; scissors beats paper; paper beats rock.
- A round where both players choose the same move is a draw.
- Draws do not count toward either player's win total.
- The match ends early as soon as one player has won enough rounds
  that the other player cannot possibly win the majority even if they
  win every remaining round.
- If all N rounds are played without an early exit, the player with
  more wins takes the match. Equal wins after N rounds is a draw.

## Win Threshold

A player wins the match by reaching ceil(N / 2) wins.

| N (rounds) | Wins needed |
|------------|-------------|
| 1          | 1           |
| 3          | 2           |
| 5          | 3           |
| 7          | 4           |
| 9          | 5           |

## CLI Interface

```
python solution.py play [--rounds N]
```

- Default is best-of-3 (N = 3).
- N must be an odd integer between 1 and 9 (inclusive). Reject even
  values with a clear error message.
- Prompt the player for their move each round using Typer's prompt().
  Accept "rock", "paper", or "scissors" (case-insensitive). Re-prompt
  on invalid input.

### Rich Output

After each round, display a Rich table row showing:
- Round number
- Player move
- Computer move
- Round result (Win / Loss / Draw)
- Running score: player wins | draws | computer wins

At the end of the match, display a summary panel with the final score
and the overall match result (Player Wins / Computer Wins / Draw).
