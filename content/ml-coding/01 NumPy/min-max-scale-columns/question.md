---
topic: "NumPy"
difficulty: Easy
---
# Min-Max Scale Columns

**Topic:** NumPy · **Difficulty:** Easy

## Problem

Given a 2-D float array `x` of shape `(n, d)`, rescale every column independently to the range `[0, 1]`: each value `v` in column `j` becomes `(v - min_j) / (max_j - min_j)`, where `min_j` and `max_j` are that column's minimum and maximum.

If a column is constant (`max_j == min_j`), every value in it becomes `0.0`. Return a new float array of the same shape, and don't use Python loops over rows or columns.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [[1.0, 10.0], [3.0, 10.0], [2.0, 10.0]]
Output: [[0.00000,0.00000],[1.00000,0.00000],[0.50000,0.00000]]
```

**Example 2**
```text
Input: x = [[-5.0, 0.0], [5.0, 4.0]]
Output: [[0.00000,0.00000],[1.00000,1.00000]]
```

## Constraints

- `1 <= n, d <= 10^3`
- `-10^6 <= x[i][j] <= 10^6`
