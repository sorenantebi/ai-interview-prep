---
topic: "NumPy"
difficulty: Medium
---
# Replace Outliers

**Topic:** NumPy · **Difficulty:** Medium

## Problem

Given a 2-D float array `x` of shape `(n, d)`, treat each column separately. A value is an **outlier** if it is more than 3 standard deviations from its column's mean, i.e. `|v - mean_j| > 3 * std_j`, using the population standard deviation (`ddof=0`). Mean, standard deviation and median are all computed on the original column, outliers included.

Return a new float array where every outlier is replaced by its column's median; all other values are unchanged. Don't modify `x`, and don't use Python loops over rows or columns.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [[1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [1.0, 5.0], [1.0, 6.0], [100.0, 5.0]]
Output: [[1.00000,5.00000],[1.00000,6.00000],[1.00000,5.00000],[1.00000,6.00000],[1.00000,5.00000],[1.00000,6.00000],[1.00000,5.00000],[1.00000,6.00000],[1.00000,5.00000],[1.00000,6.00000],[1.00000,5.00000]]
```

**Example 2**
```text
Input: x = [[1.0, 2.0], [3.0, 4.0]]
Output: [[1.00000,2.00000],[3.00000,4.00000]]
```

## Constraints

- `1 <= n, d <= 10^3`
- A constant column has standard deviation `0` and no outliers.
