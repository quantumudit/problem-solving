---
platform: misc
problem_id: "0002"
slug: data_explorer
difficulty: null
link: ""
dataset: none
---

# Data Explorer

Three data utility functions exposed as a Typer CLI application. All logic
lives in `utils.py`; `solution.py` handles only CLI wiring and Rich display.
Sample datasets are embedded directly in `solution.py`.

## Constraints

- Use **list comprehension** for `filter_students` -- no `filter()` + `lambda`
- Use **dict comprehension** for character frequency and sales aggregation
- Use **set comprehension** to derive unique products before aggregating
- Use **`str.count()`** for character counting -- no `collections` library
- Use **`sorted()`** with `lambda x: -x[1]` to rank results by value descending
- All logic (counting, filtering, sorting, aggregation) must live in `utils.py`
- `solution.py` only iterates pre-processed results -- no sorting or aggregation
- Display all results using **Rich tables** and **Rich panels**
- All CLI inputs use `typer.Option` with `prompt=` for interactive fallback

---

## Functions to Implement (`utils.py`)

### 1. count_chars

Count the frequency of every character in a string. Return results as a list
of `(character, count)` tuples sorted by count descending.

```
count_chars(text: str, ignore_case: bool = True) -> list[tuple[str, int]]
```

- All characters are counted -- letters, digits, spaces, punctuation
- When `ignore_case=True` (default), convert to lowercase before counting
- Use a dict comprehension with `set(processed)` for unique chars and
  `processed.count(char)` for the count of each
- Sort with `sorted(..., key=lambda x: -x[1])` so the most frequent char
  comes first

| Input          | ignore_case | Output (sorted by count desc)               |
|----------------|-------------|---------------------------------------------|
| "hello"        | True        | [("l",2), ("h",1), ("e",1), ("o",1)]        |
| "aab"          | True        | [("a",2), ("b",1)]                          |
| "Hello World"  | True        | [("l",3), ("o",2), ("h",1), ...]            |
| "Hello World"  | False       | [("l",3), ("o",2), ("H",1), ("W",1), ...]   |

### 2. filter_students

Filter a list of student records, keeping only those strictly younger than
a given age limit. Use a list comprehension.

```
filter_students(students: list[dict], age_limit: int = 21) -> list[dict]
```

Each student record contains at least:
- `"name"` (str)
- `"age"`  (int)

```python
students = [
    {"name": "Alice", "age": 20},
    {"name": "Bob",   "age": 25},
    {"name": "Carol", "age": 18},
]
filter_students(students, age_limit=21)
# -> [{"name": "Alice", "age": 20}, {"name": "Carol", "age": 18}]
```

### 3. get_ranked_sales

Aggregate total sales per product and return all products ranked by total
sales descending as a list of `(product, total)` tuples.

```
get_ranked_sales(transactions: list[dict]) -> list[tuple[str, float]]
```

Each transaction contains at least:
- `"product"` (str)
- `"sales"`   (int or float)

Use a dict comprehension to build the totals:
- Drive the outer comprehension off a **set comprehension** of unique product names
- Use `sum()` with a generator expression to aggregate matching rows per product
- Sort the result with `sorted(..., key=lambda x: -x[1])`

```python
transactions = [
    {"product": "Widget", "sales": 300},
    {"product": "Gadget", "sales": 450},
    {"product": "Widget", "sales": 200},
    {"product": "Gadget", "sales": 100},
]
get_ranked_sales(transactions)
# -> [("Gadget", 550.0), ("Widget", 500.0)]
```

The first element of the returned list is always the top-selling product.

---

## Sample Datasets (`solution.py`)

Define these as module-level constants in `solution.py`.

```python
STUDENTS: list[dict] = [
    {"name": "Alice",  "age": 20},
    {"name": "Bob",    "age": 25},
    {"name": "Carol",  "age": 18},
    {"name": "David",  "age": 22},
    {"name": "Eve",    "age": 19},
    {"name": "Frank",  "age": 30},
    {"name": "Grace",  "age": 17},
]

TRANSACTIONS: list[dict] = [
    {"product": "Widget",      "sales": 300},
    {"product": "Gadget",      "sales": 450},
    {"product": "Widget",      "sales": 200},
    {"product": "Gadget",      "sales": 100},
    {"product": "Doohickey",   "sales": 620},
    {"product": "Doohickey",   "sales":  80},
    {"product": "Thingamajig", "sales": 390},
]
```

---

## CLI Interface

All commands use `typer.Option` with a `prompt=` fallback. Running a command
without flags prompts the user interactively.

```
python solution.py chars --text "Hello World"
python solution.py chars --text "Hello World" --case-sensitive
python solution.py students --limit 22
python solution.py top-product
```

### chars

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--text` | `-t` | (required) | Text to analyse |
| `--ignore-case` / `--case-sensitive` | -- | `--ignore-case` | Case handling toggle |

Display a Rich table with columns **Character** (center) and **Count** (right).
Rows are already sorted by count descending from `count_chars`.

### students

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--limit` | `-l` | 21 | Keep students strictly younger than this age |

Display a Rich table with columns **Name** (cyan) and **Age** (right).
Show a summary line below the table: `N of M students match the filter.`
If no students match, display a Rich panel with a warning instead.

### top-product

No flags. Operates on the embedded `TRANSACTIONS` dataset.

Display a Rich table with columns **Rank** (dim), **Product**, and
**Total Sales** (right, formatted as `$N,NNN`). Highlight the winner row
in bold green. Follow with a Rich panel showing the winner name and total.
