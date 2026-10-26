---
topic: "NumPy"
difficulty: Medium
---
# Cosine Similarity Matrix

**Topic:** NumPy · **Difficulty:** Medium

## Problem

Given two 2-D float arrays `a` of shape `(n, d)` and `b` of shape `(m, d)`, return the `(n, m)` array of cosine similarities: entry `[i, j]` is `a[i]·b[j] / (|a[i]| · |b[j]|)`.

If either row is the zero vector, its similarity is defined as `0.0`. No Python loops over rows.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: a = [[1.0, 0.0], [1.0, 1.0]], b = [[2.0, 0.0], [0.0, 3.0]]
Output: [[1.00000,0.00000],[0.70711,0.70711]]
```

**Example 2**
```text
Input: a = [[0.0, 0.0], [3.0, 4.0]], b = [[-3.0, 4.0]]
Output: [[0.00000],[0.28000]]
```

## Constraints

- `1 <= n, m <= 2000`
- `1 <= d <= 512`
