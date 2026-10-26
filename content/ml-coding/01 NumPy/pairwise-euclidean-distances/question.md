---
topic: "NumPy"
difficulty: Medium
---
# Pairwise Euclidean Distances

**Topic:** NumPy · **Difficulty:** Medium

## Problem

Given two 2-D float arrays `a` of shape `(n, d)` and `b` of shape `(m, d)`, return the `(n, m)` array whose entry `[i, j]` is the Euclidean distance between row `a[i]` and row `b[j]`.

Use broadcasting or matrix products; no Python loops over rows. If you use the expansion `|a|² + |b|² - 2·a·b`, clip tiny negative values to `0` before the square root. Answers are accepted within `1e-4`.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: a = [[0.0, 0.0], [3.0, 4.0]], b = [[0.0, 0.0]]
Output: [[0.00000],[5.00000]]
```

**Example 2**
```text
Input: a = [[1.0, 1.0]], b = [[1.0, 1.0], [4.0, 5.0], [1.0, -2.0]]
Output: [[0.00000,5.00000,3.00000]]
```

## Constraints

- `1 <= n, m <= 2000`
- `1 <= d <= 256`
- `-100 <= a[i][k], b[j][k] <= 100`
