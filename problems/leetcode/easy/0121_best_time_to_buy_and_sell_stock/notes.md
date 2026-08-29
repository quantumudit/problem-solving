---
platform: leetcode
problem_id: "0121"
slug: best_time_to_buy_and_sell_stock
difficulty: easy
difficulty_rating: easy
language: [python]
topics: [two_pointers, sliding_window]
date_solved: 2026-08-29
revisit: false
---

## What you initially got wrong

Your first attempt had extra state:

```python
buy = 0
sell = 0
```

This caused a bug for `prices = [1, 2]` because you calculated:

```
profit = sell - buy = 2 - 0 = 2   # wrong
```

instead of `2 - 1 = 1`.

The insight: `buy` is always `prices[l]`, so you don't need `buy` or `sell` variables at all.

## Pattern you learned

This is a variable-size sliding window, but unlike the substring problems, the window
isn't maintaining a validity constraint. Instead, it maintains this invariant:

`l` always points to the minimum price seen so far.

As `r` moves:
- If a cheaper buying opportunity appears: move `l` to `r`
- Otherwise: update max profit as `prices[r] - prices[l]`

## Recognition rule

Best Time to Buy and Sell Stock:
- One pass through the array
- Left pointer = minimum value seen so far
- Right pointer scans future prices
- Update maximum profit
