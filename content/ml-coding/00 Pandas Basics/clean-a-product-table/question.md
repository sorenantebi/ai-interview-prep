---
topic: "Pandas Basics"
difficulty: Easy
---
# Clean a Product Table

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

You receive a `pd.DataFrame` `df` with product records, the name of one column `drop_col` that is not needed, and a list `required` of column names that must not contain missing values (`NaN`/`None`).

Write `clean_table(df, drop_col, required)` that returns a new DataFrame where:

1. the column `drop_col` has been removed,
2. every row that has a missing value in **any** of the columns in `required` has been removed (missing values in other columns are fine and stay),
3. the index is reset to `0, 1, 2, ...` (the old index is discarded, not kept as a column).

The input must not be modified. The column order and row order of the remaining data stay as they were.

Calls to practise: `DataFrame.drop(columns=...)`, `DataFrame.dropna(subset=...)` and `DataFrame.reset_index(drop=True)`. No Python loops are needed.

## Examples

**Example 1**
```text
Input: df = {"id": [1, 2, 3, 4], "price": [9.5, null, 3.0, 7.25], "stock": [5, 2, null, 1], "note": ["a", "b", "c", "d"]}, drop_col = "note", required = ["price"]
Output: {"id":[1,3,4],"price":[9.50000,3.00000,7.25000],"stock":[5.00000,null,1.00000]}
Explanation: Row 1 has no price and is removed. Row 2 has no stock, but stock is not required, so it stays.
```

**Example 2**
```text
Input: df = {"id": [1, 2, 3, 4], "price": [9.5, null, 3.0, 7.25], "stock": [5, 2, null, 1], "note": ["a", "b", "c", "d"]}, drop_col = "note", required = ["price", "stock"]
Output: {"id":[1,4],"price":[9.50000,7.25000],"stock":[5.00000,1.00000]}
```

**Example 3**
```text
Input: df = {"a": [1, 2], "b": [3, 4], "c": [5, 6]}, drop_col = "c", required = ["a"]
Output: {"a":[1,2],"b":[3,4]}
Explanation: Nothing is missing, so only the column is dropped.
```

## Constraints

- `0 <= len(df) <= 10^4`
- `drop_col` is a column of `df` and is not in `required`.
- Every name in `required` is a column of `df`.
