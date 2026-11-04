---
topic: "NumPy Basics"
difficulty: Easy
---
# Range Grid

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

This is a fundamentals drill. Practise `np.arange` and `reshape`, including `-1` as a size in `reshape`.

Write a function `range_grid(start, stop, rows)` that receives three Python ints and returns a 2-D integer array with `rows` rows. It holds the numbers `start, start + 1, ..., stop - 1` (what `np.arange(start, stop)` gives you) filled row by row. You are not given the number of columns: let `reshape` work it out with `-1`.

The input is always valid: `stop - start` is a positive multiple of `rows`.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: start = 0, stop = 6, rows = 2
Output: [[0,1,2],[3,4,5]]
Explanation: np.arange(0, 6) has 6 elements, so 2 rows means 3 columns.
```

**Example 2**
```text
Input: start = 3, stop = 7, rows = 4
Output: [[3],[4],[5],[6]]
Explanation: 4 elements in 4 rows gives a single column.
```

**Example 3**
```text
Input: start = -2, stop = 4, rows = 3
Output: [[-2,-1],[0,1],[2,3]]
```

## Constraints

- `-10^6 <= start < stop <= 10^6`
- `1 <= rows <= stop - start`
- `(stop - start) % rows == 0`
