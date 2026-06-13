---
platform: misc
problem_id: "0002"
slug: data_explorer
difficulty: null
difficulty_rating: easy
language: [python]
topics: [aggregation, filtering, sorting, string_ops, lambda_functions, list_comprehensions]
date_solved: 2026-06-13
revisit: false
---

# Notes

## Sorting a Dict by Value (Descending) with `sorted()` and `lambda`

`dict.items()` returns a view of `(key, value)` pairs, which `sorted()` treats as
a list of 2-tuples. The sort key indexes into each tuple.

```python
freq = {"l": 3, "h": 1, "e": 1, "o": 1}

# ascending by value (default)
sorted(freq.items(), key=lambda x: x[1])
# -> [("h", 1), ("e", 1), ("o", 1), ("l", 3)]

# descending by value -- negate the value
sorted(freq.items(), key=lambda x: -x[1])
# -> [("l", 3), ("h", 1), ("e", 1), ("o", 1)]
```

`x[0]` is the key, `x[1]` is the value. Negating `x[1]` flips the sort order
without needing `reverse=True`. Both approaches are equivalent:

```python
sorted(freq.items(), key=lambda x: -x[1])           # negate
sorted(freq.items(), key=lambda x: x[1], reverse=True)  # reverse flag
```

The negation form (`-x[1]`) is marginally more compact; the `reverse=True` form
is more explicit about intent.

---

## `Counter` vs Manual Dict Comprehension for Character Frequency

Both produce a character frequency mapping, but differ in how the result is ordered
and how they count.

| Aspect          | `Counter.most_common()`                        | Dict comprehension + `str.count()`             |
|-----------------|------------------------------------------------|------------------------------------------------|
| Return type     | `list[tuple[str, int]]`, sorted by count desc  | `dict[str, int]`, unordered (needs `sorted()`) |
| How it counts   | Single O(n) pass over the string               | `str.count()` per unique char -- O(n * k)      |
| Imports needed  | `from collections import Counter`              | None                                           |
| Readability     | Concise, intent is clear                       | More explicit, no hidden behaviour             |

```python
from collections import Counter

# Counter approach
Counter("hello").most_common()
# -> [("l", 2), ("h", 1), ("e", 1), ("o", 1)]

# Manual dict comprehension
processed = "hello"
freq = {char: processed.count(char) for char in set(processed)}
sorted(freq.items(), key=lambda x: -x[1])
# -> [("l", 2), ("h", 1), ("e", 1), ("o", 1)]
```

`Counter` is faster on large strings because it counts in a single pass.
The dict comprehension trades efficiency for zero imports and explicit logic.

---

## `filter()` + `lambda` vs List Comprehension

Both filter a list by a condition; the choice is mostly style.

| Aspect          | `filter()` + `lambda`                          | List comprehension                             |
|-----------------|------------------------------------------------|------------------------------------------------|
| Return type     | `filter` iterator (needs `list()` to consume)  | `list` directly                                |
| Readability     | Reads as "filter where condition"              | Reads as "give me x where condition"           |
| Performance     | Marginally faster for large datasets           | Negligible difference in practice              |
| Python style    | Functional -- borrowed from older Python 2     | Idiomatic Python 3                             |

```python
students = [
    {"name": "Alice", "age": 20},
    {"name": "Bob",   "age": 25},
    {"name": "Carol", "age": 18},
]

# filter + lambda
list(filter(lambda s: s["age"] < 21, students))

# list comprehension (preferred)
[s for s in students if s["age"] < 21]

# both produce:
# [{"name": "Alice", "age": 20}, {"name": "Carol", "age": 18}]
```

List comprehension is the idiomatic Python 3 choice. `filter()` is useful when
passing a pre-defined function rather than a lambda, which avoids the inline
anonymous function entirely:

```python
def is_young(s: dict) -> bool:
    return s["age"] < 21

list(filter(is_young, students))
```

---

## Dictionary Comprehension for Grouped Aggregation

`get_ranked_sales` uses a dict comprehension to aggregate sales per product.
The trick is driving the outer comprehension off a set of unique products, then
using a generator expression inside `sum()` to filter and add matching rows.

```python
transactions = [
    {"product": "Widget", "sales": 300},
    {"product": "Gadget", "sales": 450},
    {"product": "Widget", "sales": 200},
    {"product": "Gadget", "sales": 100},
]

totals = {
    product: sum(t["sales"] for t in transactions if t["product"] == product)
    for product in {t["product"] for t in transactions}
}
# -> {"Widget": 500, "Gadget": 550}
```

Breaking it down:

```
{t["product"] for t in transactions}
```
A set comprehension that extracts unique product names -- `{"Widget", "Gadget"}`.

```
sum(t["sales"] for t in transactions if t["product"] == product)
```
For each unique product, a generator expression that scans all transactions,
keeps only matching rows, and sums their sales.

The outer dict comprehension pairs each product name with its aggregated total.

Note: this is O(n * k) where k is the number of unique products, because it
scans all transactions once per unique product. A single-pass loop with
`dict.get()` is O(n), but the comprehension form is more concise and readable
for typical dataset sizes.
