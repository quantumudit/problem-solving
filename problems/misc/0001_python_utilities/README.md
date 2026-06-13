---
platform: misc
problem_id: "0001"
slug: python_utilities
difficulty: null
link: ""
dataset: none
---

# Python Utilities

A command-line toolkit that bundles four small utility functions into a
Typer application with Rich-formatted output. Each function is a separate
subcommand.

## Functions to Implement

### 1. minutes_to_seconds

Convert a number of minutes to the equivalent number of seconds.

- Input: a non-negative integer (minutes)
- Output: an integer (seconds)

| Input | Output |
|-------|--------|
| 2     | 120    |
| 0     | 0      |
| 90    | 5400   |

### 2. sum_two_numbers

Return the sum of two numeric values.

- Input: two values, int or float
- Output: their sum (int or float)

| a    | b    | Output |
|------|------|--------|
| 3    | 4    | 7      |
| 2.5  | 1.5  | 4.0    |
| -3   | 3    | 0      |

### 3. fizzbuzz

Return the FizzBuzz sequence from 1 to n (inclusive) as a list of strings.

Rules:
- Multiple of 3 only  -> "Fizz"
- Multiple of 5 only  -> "Buzz"
- Multiple of both    -> "FizzBuzz"
- Everything else     -> the number as a string

- Input: a positive integer n
- Output: a list of strings

Example (n = 15):

```
["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
 "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
```

### 4. sign_and_parity

Return the sign and parity of an integer as a 2-tuple.

- Input: an integer
- Output: (sign, parity)
  - sign   : "positive" | "negative" | "zero"
  - parity : "even" | "odd"

| Input | Output                   |
|-------|--------------------------|
| 7     | ("positive", "odd")      |
| -4    | ("negative", "even")     |
| 0     | ("zero", "even")         |

## CLI Interface

Each function is exposed as a Typer subcommand. All output is rendered
inside a Rich panel or table with clear labels.

```
python solution.py convert 90        # minutes -> seconds
python solution.py add 2.5 1.5       # sum of two numbers
python solution.py fizzbuzz 20       # FizzBuzz sequence up to 20
python solution.py parity 7          # sign and parity of 7
```
