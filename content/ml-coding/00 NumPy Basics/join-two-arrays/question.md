---
topic: "NumPy Basics"
difficulty: Easy
---
# Join Two Arrays

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

This is a fundamentals drill on joining arrays. The calls to practise are `np.concatenate`, `np.vstack`, `np.hstack` and `np.stack`.

Write a function `join_arrays(a, b)` that receives two 2-D float arrays `a` and `b` of the same shape `(m, n)` and returns a tuple of three arrays:

1. `vertical`: `a` on top of `b`, shape `(2m, n)` (practise `np.vstack`, or `np.concatenate` with `axis=0`).
2. `horizontal`: `a` next to `b`, shape `(m, 2n)` (practise `np.hstack`, or `np.concatenate` with `axis=1`).
3. `stacked`: `a` and `b` joined along a **new last axis**, shape `(m, n, 2)`, so that `stacked[i, j]` is `[a[i, j], b[i, j]]` (practise `np.stack` with `axis=2`).

The intended solution is one line per result.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: a = [[1.0, 2.0], [3.0, 4.0]], b = [[5.0, 6.0], [7.0, 8.0]]
Output: [[[1.00000,2.00000],[3.00000,4.00000],[5.00000,6.00000],[7.00000,8.00000]],[[1.00000,2.00000,5.00000,6.00000],[3.00000,4.00000,7.00000,8.00000]],[[[1.00000,5.00000],[2.00000,6.00000]],[[3.00000,7.00000],[4.00000,8.00000]]]]
Explanation: the shapes are (4, 2), (2, 4) and (2, 2, 2).
```

**Example 2**
```text
Input: a = [[1.0, 2.0, 3.0]], b = [[4.0, 5.0, 6.0]]
Output: [[[1.00000,2.00000,3.00000],[4.00000,5.00000,6.00000]],[[1.00000,2.00000,3.00000,4.00000,5.00000,6.00000]],[[[1.00000,4.00000],[2.00000,5.00000],[3.00000,6.00000]]]]
Explanation: the shapes are (2, 3), (1, 6) and (1, 3, 2).
```

## Constraints

- `a` and `b` are float arrays with the same shape `(m, n)`
- `1 <= m, n <= 100`
