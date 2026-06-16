difficulty_rating: easy

## My Learnings

- Using of difficulty ranges as dictionary and then accessing it via tuple rather than going into a if..else loop:

```python
DIFFICULTY_RANGES = {
    "easy": (1, 50),
    "medium": (1, 100),
    "hard": (1, 500),
}

low, high = DIFFICULTY_RANGES["medium"]
```

So, for complex if..else or, nested if..else we can use this trick instead.

