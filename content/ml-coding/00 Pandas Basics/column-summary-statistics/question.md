---
topic: "Pandas Basics"
difficulty: Easy
---
# Column Summary Statistics

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

Write `column_stats(df, col)`, which receives a `pd.DataFrame` `df` and the name `col` of one numeric column in it. Return a `pd.Series` with the **mean, min, max and sum** of that column, with index labels `"mean"`, `"min"`, `"max"`, `"sum"` in exactly this order. The Series must be named after the column (`name == col`).

Missing values (`NaN`) are skipped, which is the pandas default.

Calls to practise: select a column with `df[col]` and compute several statistics at once with `Series.agg([...])`. The whole solution fits in one or two lines. There is no need for loops. Also have a look at `Series.describe()` to see how it differs.

## Examples

**Example 1**
```text
Input: df = {"a": [1, 2, 3, 4], "b": [10, 20, 30, 40]}, col = "a"
Output: {"mean":2.50000,"min":1.00000,"max":4.00000,"sum":10.00000}
```

**Example 2**
```text
Input: df = {"price": [2.5, 0.5, 4.0], "qty": [1, 2, 3]}, col = "price"
Output: {"mean":2.33333,"min":0.50000,"max":4.00000,"sum":7.00000}
Explanation: only the "price" column is used; "qty" is ignored.
```

**Example 3**
```text
Input: df = {"x": [1.0, null, 3.0]}, col = "x"
Output: {"mean":2.00000,"min":1.00000,"max":3.00000,"sum":4.00000}
Explanation: the missing value is skipped, so the mean is over two values.
```

## Constraints

- `1 <= len(df) <= 10^5`
- `col` is the name of a numeric column of `df`
- The column contains at least one non-missing value
