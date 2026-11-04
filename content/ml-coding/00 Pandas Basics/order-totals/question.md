---
topic: "Pandas Basics"
difficulty: Easy
---
# Order Totals

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

This is a fundamentals drill. Practise these two calls:

- `pd.DataFrame(...)` to build a DataFrame from a dict of lists
- column access and assignment (`df["a"]`, `df["new"] = ...`) to add a column computed from two others

Write `add_total(data)`. `data` is a dict mapping column names to equally long lists. It always has the keys `"item"` (list of `str`), `"price"` (list of `float`, may contain `NaN`) and `"quantity"` (list of `int`).

Return a `pd.DataFrame` built from `data` with one extra column, `"total"`, equal to `price * quantity` in every row. The original three columns stay in their original order, and `"total"` comes last.

Do not loop over the rows; use a vectorised column operation.

## Examples

**Example 1**
```text
Input: data = {"item": ["pen", "book"], "price": [1.5, 12.0], "quantity": [4, 2]}
Output: {"item":["pen","book"],"price":[1.50000,12.00000],"quantity":[4,2],"total":[6.00000,24.00000]}
Explanation: 1.5 * 4 = 6.0 and 12.0 * 2 = 24.0
```

**Example 2**
```text
Input: data = {"item": ["tea"], "price": [2.5], "quantity": [0]}
Output: {"item":["tea"],"price":[2.50000],"quantity":[0],"total":[0.00000]}
Explanation: a quantity of 0 gives a total of 0.0
```

**Example 3**
```text
Input: data = {"item": ["cup", "lid"], "price": [3.0, NaN], "quantity": [2, 5]}
Output: {"item":["cup","lid"],"price":[3.00000,null],"quantity":[2,5],"total":[6.00000,null]}
Explanation: a missing price stays missing in the total
```

## Constraints

- `1 <= n <= 10^3`, where `n` is the length of each list
- `"price"` values are finite floats or `NaN`; `"quantity"` values are non-negative integers
