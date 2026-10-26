---
topic: "NumPy"
difficulty: Medium
---
# Top-K per Row

**Topic:** NumPy · **Difficulty:** Medium

## Problem

Given a 2-D array `x` of shape `(n, d)` and an integer `k` (`1 <= k <= d`), return an integer array of shape `(n, k)`: row `i` holds the column indices of the `k` largest values in `x[i]`, ordered from largest value to smallest. When values are equal, the lower column index comes first.

No Python loops over rows.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [[0.1, 0.9, 0.5], [3.0, 3.0, 1.0]], k = 2
Output: [[1,2],[0,1]]
```

**Example 2**
```text
Input: x = [[5.0, 1.0, 5.0, 7.0]], k = 3
Output: [[3,0,2]]
```

## Constraints

- `1 <= n <= 10^4`
- `1 <= k <= d <= 10^4`
