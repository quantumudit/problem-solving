difficulty_rating: easy

## My Learnings

The use of `winning_pairs` and then, using it in a ternary operator is really smart approach to ditch if..elif..else statements

```python

winning_pairs = {
        ("rock", "scissors"),
        ("scissors", "paper"),
        ("paper", "rock"),
}

winner = "human" if (human, robot) in winning_pairs else "robot"
```

Defining `CHOICES` set and using it to validate user input and using it inside `random.choice()` is really a smart move.

