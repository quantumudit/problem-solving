---
platform: alteryx_community
problem_id: "0014"
slug: date_parsing
difficulty: hard
difficulty_rating: hard
language: [pandas]
topics: [string_ops, datetime]
date_solved: 2026-06-26
revisit: true
---

# Notes

Revisit to add Polars solution.

## Regex Alternation with `|`

The `|` operator in regex means "match either the left pattern or the right pattern".
Wrapping both in a single capturing group lets `str.extract()` return whichever branch matched.

```python
pattern = r"(\d{1,2}-\w{3,4}-\d{2,4}|\w{3}\s\d{1,2},?\s\d{4})"
#           |<-- DD-MON-YY(YY) --->|<----- Mon DD[,] YYYY ------>|
```

---

## Optional Characters with `?`

`?` makes the preceding token optional (0 or 1 occurrences). `\d{1,2},?` matches
a day number with or without a trailing comma -- covering both "Nov 16, 1900" and
"Jan 5 2000" with a single pattern rather than two separate branches.

---

## Extracting Dates from Text with `str.extract()`

`str.extract(pattern)` applies a regex to each element of a string Series and returns
the first capturing group as a new Series. If nothing matches, the row gets NaN.

```python
text_df["date_str"] = text_df["Text"].str.extract(pattern)
```

Only the first match per row is returned. For all matches, use `str.extractall()`.

---

## Mixed-Format Date Parsing

`pd.to_datetime(..., format="mixed")` infers the date format independently for each
row rather than enforcing a single format across the whole column. This handles columns
where dates are stored in multiple formats.

```python
text_df["parsed_date"] = pd.to_datetime(text_df["date_str"], format="mixed", errors="coerce")
```

`errors="coerce"` turns any unparseable values into NaT instead of raising.

---

## Fixing 2-Digit Year Ambiguity with `pd.DateOffset`

2-digit years like "00" can be parsed as 2100 instead of 2000. `pd.DateOffset`
applies a relative date shift while respecting calendar conventions (e.g., leap years).

```python
text_df.loc[future_mask, "parsed_date"] -= pd.DateOffset(years=100)
```

This is safer than subtracting a fixed number of days, since a century spans a
different number of days depending on how many leap years it crosses.
