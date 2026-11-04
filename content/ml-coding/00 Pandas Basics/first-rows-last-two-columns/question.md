---
topic: "Pandas Basics"
difficulty: Easy
---
# First Rows, Last Two Columns

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

Write a function `top_left_slice(df, n)` that receives a `pd.DataFrame` `df` (at least two columns, any dtypes) and an integer `n`. It must return a new `pd.DataFrame` that contains the **first `n` rows** and the **last two columns** of `df`, selected **by position**.

The row index and the column names must be kept unchanged (do not reset the index), and the column order must stay as in `df`.

**Calls to practise:** `DataFrame.iloc` with a slice for the rows and a negative slice for the columns. Select by position, not by label: don't use `.loc`, `.head()` or column names. The whole solution fits in one line.

## Examples

**Example 1**
```text
Input: df = {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}, n = 2
Output: {"b": [4, 5], "c": [7, 8]}
Explanation: the first two rows, and the last two columns "b" and "c".
```

**Example 2**
```text
Input: df = {"x": [1.5, 2.5], "y": [0.5, 1.0], "z": [3.0, 4.0], "w": [9.0, 8.0]}, n = 1
Output: {"z": [3.00000], "w": [9.00000]}
```

**Example 3**
```text
Input: df = {"p": [1, 2, 3, 4], "q": [5, 6, 7, 8]}, n = 3
Output: {"p": [1, 2, 3], "q": [5, 6, 7]}
Explanation: the frame has only two columns, so both are kept.
```

## Constraints

- `2 <= number of columns <= 100`
- `0 <= n <= number of rows <= 10^4`
