---
platform: misc
problem_id: "0003"
slug: calculator
difficulty: null
link: ""
dataset: none
---

# Calculator

Build an interactive REPL calculator in two parts:

1. A `Calculator` class that owns all computation and history. It takes a `mode` at
   construction that determines how inputs are processed for the session.
2. A Typer REPL that asks the user to pick a mode at startup, then loops on the
   appropriate input flow for that mode.

The class does all the work. The REPL only handles prompting, command dispatch, and
display.

## Part 1 -- Calculator Class

`Calculator(mode)` takes one of two modes and maintains a shared history list across
all computations in the session regardless of mode.

```
Calculator(mode: "expression" | "manual")
```

### Methods

| Method                          | Description                                         |
|---------------------------------|-----------------------------------------------------|
| evaluate(expression)            | Parse and evaluate a free-form math string          |
| compute(a, b, operator)         | Apply a binary operator to two numbers              |
| get_history()                   | Return the full history list                        |
| clear_history()                 | Clear all history entries                           |

Both `evaluate` and `compute` return a plain string -- either the result or an error
message starting with `"Error:"`. They also append a formatted entry to history on
success. The REPL checks for `"Error:"` to decide how to display the result; it never
touches history directly.

---

### evaluate(expression: str) -> str

Used in expression mode. Safely parses and evaluates a free-form math string.

**Implementation:**

1. Validate with a compiled regex. Allow only: digits, decimal points, whitespace,
   operators `+ - * / % **`, parentheses, and the function names listed below.
   Return an error string for anything else.

2. Call `eval()` with a fully restricted namespace -- no builtins, only:

```python
{"sqrt": math.sqrt, "abs": abs, "round": round}
```

3. Catch and return an error string (not raise) for `ZeroDivisionError`, `SyntaxError`,
   `NameError`, `TypeError`, and `ValueError`.

4. On success, append `"<expression> = <result>"` to history and return the result
   as a string.

**Examples:**

| Expression             | Result       |
|------------------------|--------------|
| "2 + 3"                | "5"          |
| "10 / 4"               | "2.5"        |
| "2 ** 8"               | "256"        |
| "10 % 3"               | "1"          |
| "sqrt(144)"            | "12.0"       |
| "abs(-7) + round(2.9)" | "10.0"       |
| "10 / 0"               | "Error: ..." |
| "__import__('os')"     | "Error: ..." |

---

### compute(a: int | float, b: int | float, operator: str) -> str

Used in manual mode. Applies a binary operator to two numbers.

Supported operators: `+  -  *  /  %  **`

Returns an error string for an unrecognised operator or division/modulo by zero.
On success, appends `"<a> <operator> <b> = <result>"` to history and returns the
result as a string.

---

## Part 2 -- Typer REPL

An interactive REPL launched via:

```
python solution.py repl
```

### Startup

1. Prompt the user to choose a mode:

```
Mode (expression / manual):
```

   Re-prompt on invalid input.

2. Create a `Calculator` instance with the chosen mode.

3. Display a Rich panel with instructions for the chosen mode.

### Expression mode loop

Each iteration prompts for a single expression string:

```
> 2 ** 8
256
> sqrt(144)
12.0
```

### Manual mode loop

Each iteration prompts for three inputs in sequence:

```
  First Number : 10
  Second Number: 3
  Operator     : %
1
```

Special commands (`history`, `clear`, `exit`, `quit`) are accepted at the `First Number`
prompt so the user is not forced to complete a computation to exit or check history.

### Commands (both modes)

| Command        | Action                              |
|----------------|-------------------------------------|
| history        | Display a Rich table of past results|
| clear          | Clear the history                   |
| exit / quit    | End the session                     |

Failed expressions or invalid inputs print an error in red and continue the loop
without crashing.
