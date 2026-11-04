---
topic: "NumPy Basics"
difficulty: Easy
---
# Multiplication Table with Broadcasting

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

Write a function `multiplication_table(n, m)` that returns the `n x m` multiplication table as a NumPy array. Entry `[i, j]` must equal `(i + 1) * (j + 1)`, so the first row is `1, 2, ..., m` and the first column is `1, 2, ..., n`.

The function receives two integers `n` (number of rows) and `m` (number of columns) and returns a 2-D `np.ndarray` of shape `(n, m)`.

Calls to practise: `np.arange` to create the two vectors `1..n` and `1..m`, and broadcasting with `[:, None]` (or `np.newaxis`) to turn one of them into a column vector, so that a single multiplication produces the whole table. Don't use Python loops.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: n = 3, m = 4
Output: [[1.00000,2.00000,3.00000,4.00000],[2.00000,4.00000,6.00000,8.00000],[3.00000,6.00000,9.00000,12.00000]]
Explanation: row i is (i + 1) times [1, 2, 3, 4]
```

**Example 2**
```text
Input: n = 1, m = 1
Output: [[1.00000]]
```

**Example 3**
```text
Input: n = 2, m = 3
Output: [[1.00000,2.00000,3.00000],[2.00000,4.00000,6.00000]]
```

## Constraints

- `1 <= n, m <= 10^3`
