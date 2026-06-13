---
platform: misc
problem_id: "0002"
slug: data_explorer
difficulty: null
link: ""
dataset: none
---

# Data Explorer

Three data utility functions exposed as Typer subcommands. Results are
displayed using Rich tables. Sample datasets for students and transactions
are embedded directly in the solution.

## Functions to Implement

### 1. count_chars

Count the frequency of every character in a string and return a dict
mapping each character to its count. All characters (letters, digits,
spaces, punctuation) are counted; nothing is dropped.

- Input: a string
- Output: dict[str, int]

| Input       | Output                              |
|-------------|-------------------------------------|
| "hello"     | {'h':1, 'e':1, 'l':2, 'o':1}       |
| "aab"       | {'a':2, 'b':1}                      |
| "abc abc"   | {'a':2, 'b':2, 'c':2, ' ':1}       |

### 2. filter_students

Filter a list of student dicts, keeping only those strictly younger than
a given age limit.

Each student record contains at least:
- "name" (str)
- "age"  (int)

- Input: list[dict], age_limit: int
- Output: list[dict] where age < age_limit

```python
students = [
    {"name": "Alice", "age": 20},
    {"name": "Bob",   "age": 25},
    {"name": "Carol", "age": 18},
]
filter_students(students, age_limit=21)
# -> [{"name": "Alice", "age": 20}, {"name": "Carol", "age": 18}]
```

### 3. find_product_with_highest_sales

Identify the product with the highest total sales across all transactions.

Each transaction contains at least:
- "product" (str)
- "sales"   (int or float)

- Input: list[dict]
- Output: str -- name of the top-selling product

If two products tie, returning either is acceptable.

```python
transactions = [
    {"product": "Widget", "sales": 300},
    {"product": "Gadget", "sales": 450},
    {"product": "Widget", "sales": 200},
    {"product": "Gadget", "sales": 100},
]
find_product_with_highest_sales(transactions)
# -> "Gadget"  (total: 550 vs Widget's 500)
```

## CLI Interface

Each function is a Typer subcommand. The `chars` command accepts a string
argument; `students` and `top-product` operate on built-in sample datasets.

```
python solution.py chars "hello world"
python solution.py students --limit 22
python solution.py top-product
```

Display results in Rich tables with column headers and row formatting.
