---
platform: misc
problem_id: "0001"
slug: python_utilities
difficulty: null
link: ""
dataset: none
---

# Python Utilities

Four small utility functions bundled into a Typer CLI application with
Rich-formatted output. All logic lives in `utils.py`; `solution.py` handles
only CLI wiring and display.

## Constraints

- Use **chained ternary** for `sign_and_parity` -- no if/elif/else block
- Use **`int | float`** union type hints (Python 3.10+) -- no `Union[]` or `Optional[]`
- Use **`isinstance()` with `|`** for runtime type checks
- All four functions must raise `ValueError` with a descriptive message on bad input
- All CLI inputs use **`typer.Option`** with `prompt=` -- no `typer.Argument`
- For negative integers, pass via option flag (`--num -4` or `-n -4`) to avoid
  CLI parser treating the `-` as a flag
- Display all results using **Rich panels** (single values) or **Rich tables** (sequences)

---

## Functions to Implement (`utils.py`)

### 1. minutes_to_seconds

Convert a non-negative integer number of minutes to seconds.

```
minutes_to_seconds(minutes: int) -> int
```

Raise `ValueError` if `minutes` is not a non-negative integer.

| Input | Output |
|-------|--------|
| 2     | 120    |
| 0     | 0      |
| 90    | 5400   |

### 2. sum_two_numbers

Return the sum of two numeric values. Accept both `int` and `float` using
the `int | float` union type. Validate both inputs with `isinstance()`.

```
sum_two_numbers(num1: int | float, num2: int | float) -> int | float
```

Raise `ValueError` if either input is not an `int` or `float`.

| num1 | num2 | Output |
|------|------|--------|
| 3    | 4    | 7      |
| 2.5  | 1.5  | 4.0    |
| -3   | 3    | 0      |

### 3. fizzbuzz

Return the FizzBuzz sequence from 1 to n (inclusive) as a list of strings.

```
fizzbuzz(n: int) -> list[str]
```

Rules:
- Multiple of both 3 and 5 -> `"FizzBuzz"`
- Multiple of 3 only        -> `"Fizz"`
- Multiple of 5 only        -> `"Buzz"`
- Everything else           -> the number as a string

Raise `ValueError` if `n` is not a positive integer.

Example (n = 15):

```
["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
 "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
```

### 4. sign_and_parity

Return the sign and parity of an integer as a 2-tuple. Implement using
a **chained ternary expression** -- no if/elif/else blocks.

```
sign_and_parity(num: int) -> tuple[str, str]
```

- `sign`   : `"Positive"` | `"Negative"` | `"Zero"`
- `parity` : `"Even"` | `"Odd"`

Raise `ValueError` if `num` is not an integer.

| Input | Output                    |
|-------|---------------------------|
| 7     | ("Positive", "Odd")       |
| -4    | ("Negative", "Even")      |
| 0     | ("Zero", "Even")          |

---

## CLI Interface

All commands use `typer.Option` with a `prompt=` fallback. Running a command
without flags prompts the user interactively.

```
python solution.py convert --minutes 90
python solution.py add --num1 2.5 --num2 1.5
python solution.py fizzbuzz --limit 20
python solution.py parity --num 7
```

### convert

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--minutes` | `-m` | (required) | Number of minutes to convert |

Display: Rich panel -- `X minutes = Y seconds`

### add

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--num1` | `-a` | (required) | First number |
| `--num2` | `-b` | (required) | Second number |

Note: Typer does not support `int | float` union types. Declare both parameters
as `float` in the CLI layer -- Typer accepts integer input and coerces it.
Use `:g` format specifier in the output to suppress trailing zeros (`4.0` -> `4`).

Display: Rich panel -- `A + B = result`

### fizzbuzz

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--limit` | `-n` | (required) | Upper bound of the sequence (inclusive) |

Display: Rich table with two columns -- `n` (dim, right-aligned) and `Result`.
Color-code the Result column:

| Value     | Color   |
|-----------|---------|
| FizzBuzz  | magenta bold |
| Fizz      | green   |
| Buzz      | yellow  |
| Number    | default |

### parity

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--num` | `-n` | (required) | Integer to inspect |

For negative integers, use the flag form: `parity --num -4` or `parity -n -4`.
Running `parity` without a flag falls back to a prompt where negatives can be
typed freely.

Display: Rich panel with three rows -- Number, Sign (color-coded), Parity.

| Sign value | Color  |
|------------|--------|
| Positive   | green  |
| Negative   | red    |
| Zero       | yellow |
