---
platform: misc
problem_id: "0007"
slug: rock_paper_scissors
difficulty: null
difficulty_rating: easy
language: [python]
topics: [conditional_logic, simulation]
date_solved: 2026-06-14
revisit: false
---

# Notes

## Set of Tuples as a Win-Condition Lookup

Instead of an if/elif chain to check which move beats which, all winning combinations
can be encoded as a set of `(winner_move, loser_move)` tuples. A single membership
test then replaces all the branching:

```python
# if/elif -- a new branch for every combination
if human == "rock" and robot == "scissors":
    return "human"
elif human == "scissors" and robot == "paper":
    return "human"
elif human == "paper" and robot == "rock":
    return "human"
else:
    return "robot"

# set lookup -- all combinations declared once, membership test replaces branching
_WINNING_PAIRS = frozenset({
    ("rock", "scissors"),
    ("scissors", "paper"),
    ("paper", "rock"),
})

return "human" if (human, robot) in _WINNING_PAIRS else "robot"
```

The set is defined at module level as a `frozenset` (immutable) so it is created
once when the module loads, not rebuilt on every function call. The ternary combined
with `in` makes the intent read naturally: "if this pair is a winning pair, human
wins, otherwise robot wins."

---

## CHOICES Tuple -- One Constant, Two Purposes

Defining valid moves as a single module-level constant serves both validation and
random selection from the same source:

```python
CHOICES = ("rock", "paper", "scissors")

# validate user input
if user_input not in CHOICES:
    print(f"Invalid. Choose: {', '.join(CHOICES)}")

# pick the computer's move
computer = random.choice(CHOICES)
```

`random.choice()` accepts any sequence, so the same tuple works for both. One source
of truth means adding a new move (e.g. "lizard") only requires updating `CHOICES` --
validation and random selection both pick it up automatically.
