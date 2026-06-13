---
platform: misc
problem_id: "0003"
slug: calculator
difficulty: null
link: ""
dataset: none
---

# Calculator

An interactive REPL calculator that combines two approaches: a Calculator
class with standard arithmetic operators for structured operations, and a
safe expression evaluator that uses regex validation and eval() with a
restricted namespace for free-form expressions including math functions.

## Part 1 -- Calculator Class

A `Calculator` class that supports the four basic arithmetic operations
and maintains a history of all computations performed in the session.

### Methods

| Method            | Description                                    |
|-------------------|------------------------------------------------|
| add(a, b)         | Return a + b                                   |
| subtract(a, b)    | Return a - b                                   |
| multiply(a, b)    | Return a * b                                   |
| divide(a, b)      | Return a / b; raise ZeroDivisionError if b = 0 |
| get_history()     | Return the full history list                   |
| clear_history()   | Clear all history entries                      |

Each successful operation appends a formatted string to history:

```
"3 + 4 = 7"
"10 / 2 = 5.0"
"sqrt(16) = 4.0"
```

## Part 2 -- Safe Expression Evaluator

An `evaluate(expression: str)` function that safely parses and evaluates
a free-form math string.

### Implementation Requirements

1. Compile a regex pattern to validate the expression before evaluating.
   Only allow: digits, decimal points, arithmetic operators (+, -, *, /,
   **), parentheses, whitespace, and the names of the allowed functions
   listed below. Reject anything else.

2. Call eval() with a fully restricted namespace -- no builtins, only
   the allowed names:

```python
allowed_names = {
    "sqrt":  math.sqrt,
    "abs":   abs,
    "round": round,
}
```

3. Catch and return an error string (not raise) for:
   - Expressions that fail regex validation
   - ZeroDivisionError
   - Any other eval-time exception

### Examples

| Expression              | Result          |
|-------------------------|-----------------|
| "2 + 3"                 | 5               |
| "10 / 4"                | 2.5             |
| "2 ** 8"                | 256             |
| "sqrt(144)"             | 12.0            |
| "abs(-7) + round(2.9)"  | 10.0            |
| "sqrt(2) * round(1.5)"  | 1.414...        |
| "10 / 0"                | "Error: ..."    |
| "__import__('os')"      | "Error: ..."    |

## Part 3 -- Typer REPL

An interactive REPL that wraps the evaluator, launched via a Typer
command.

```
python solution.py repl
```

### Behavior

- On startup, display a Rich panel with usage instructions, listing
  supported operators and math functions.
- Each line of user input is passed to `evaluate()` and the result is
  printed in Rich-formatted output.
- Every successful computation is also appended to the Calculator's
  history so both the class and the evaluator share one history list.
- Special commands (case-insensitive):
  - `history` -- display a Rich table of all past computations
  - `clear`   -- clear the history
  - `exit` or `quit` -- end the REPL session
- Invalid or failed expressions show an error message without crashing.
