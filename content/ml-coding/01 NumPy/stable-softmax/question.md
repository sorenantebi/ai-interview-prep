---
topic: "NumPy"
difficulty: Easy
---
# Stable Softmax

**Topic:** NumPy · **Difficulty:** Easy

## Problem

Given a 2-D array `x` of shape `(n, k)` holding one row of scores (logits) per example, return the softmax of each row: `exp(x[i, j]) / sum_j exp(x[i, j])`. Every row of the result is non-negative and sums to 1.

Your function must stay correct for large scores such as `1000.0`, where a direct `np.exp` overflows. Don't use Python loops over the rows.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [[1.0, 2.0, 3.0]]
Output: [[0.09003,0.24473,0.66524]]
```

**Example 2**
```text
Input: x = [[1000.0, 1000.0], [0.0, -1000.0]]
Output: [[0.50000,0.50000],[1.00000,0.00000]]
Explanation: subtracting each row's maximum first keeps exp() from overflowing.
```

## Constraints

- `1 <= n, k <= 10^3`
- `-10^4 <= x[i][j] <= 10^4`
