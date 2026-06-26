---
platform: alteryx_community
problem_id: "0012"
slug: preparing_delimited_data
difficulty: easy
difficulty_rating: easy
language: [pandas, polars]
topics: [string_ops, datetime]
date_solved: 2026-06-18
revisit: true
---

## Approach

The raw input is a single CSV column (`Field_1`) where each value packs three fields
separated by commas -- a double-quoted poem title, a bare integer ID, and a single-quoted
date string:

```
"Mary had a little lamb whose fleece was white as snow",123,'16-JUN-01'
```

The task is to split on commas, strip the surrounding quote characters from the first and
third fields, and parse the date into a proper date type.

### Pandas

Split `Field_1` once with `str.split(",", expand=True)` -- the `expand=True` materializes
the result into a three-column DataFrame so each positional field is accessible by index.
Strip whitespace and quote delimiters with `str.strip()` followed by `str.strip('"')` or
`str.strip("'")`, then cast types and build the output frame directly.

### Polars

Assign `pl.col("Field_1").str.split(",")` to a variable as a lazy expression (no memory
allocation yet). Pass it into `.select()` where Polars evaluates it once and applies
`.list.get(i)` per field. `str.strip_chars(' "')` strips both spaces and double-quote
characters in a single Rust-level pass. `str.to_date()` parses directly into a `Date`
type without the intermediate `datetime64` allocation that Pandas requires.

## Pandas vs Polars

| Aspect | Pandas | Polars |
|---|---|---|
| Split result | `expand=True` materializes a DataFrame in memory | Lazy expression -- evaluated once inside `.select()` |
| Quote stripping | Two chained calls: `.str.strip()` then `.str.strip('"')` | Single call: `.str.strip_chars(' "')` removes any combo of chars |
| Date parsing | `pd.to_datetime(...).dt.date` -- allocates full timestamp, extracts date | `.str.to_date()` -- parses directly to a `Date` type |
| Output construction | `pd.DataFrame({...})` from positional index columns | `.select(...)` with aliased expressions inline |

## Tricks / New Learnings

`str.strip_chars(chars)` in Polars accepts a string of characters to strip (not a
delimiter pattern) -- `str.strip_chars(' "')` removes any leading/trailing space or
double-quote in one pass, which is cleaner than chaining two strip calls.

`str.to_date(format)` in Polars parses directly to a native `Date` type. In Pandas the
equivalent is `pd.to_datetime(..., format=...).dt.date`, which goes through a `datetime64`
array first and then extracts the date portion -- slightly wasteful for date-only data.

`pl.col(...).str.split(",")` assigned to a variable in Polars is just an expression object,
not a computed result. Polars evaluates it once during the `.select()` call and reuses the
plan for each `.list.get(i)` -- there is no repeated splitting at runtime.

## Revisit notes

Come back to write a DuckDB/SQL solution. SQL handles this cleanly with
`regexp_replace` or `trim(both '"' from col)` for quote stripping and
`strptime` for date parsing.
