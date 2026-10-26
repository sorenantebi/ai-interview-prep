---
topic: "NumPy"
difficulty: Medium
---
# Batched Bilinear Scores

**Topic:** NumPy · **Difficulty:** Medium

## Problem

You have a batch of `B` examples. For each example `b` there are `n` query vectors `q[b]` (shape `(n, d)`) and `m` key vectors `keys[b]` (shape `(m, d)`), and one shared weight matrix `w` of shape `(d, d)`.

Return the array `s` of shape `(B, n, m)` with `s[b, i, j] = q[b, i] · (w @ keys[b, j])`, i.e. `q[b] @ w @ keys[b].T` for every batch element.

Don't loop over the batch in Python: use `@`, which broadcasts over leading dimensions, together with a transpose of the keys' last two axes.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: q = [[[1.0, 0.0], [0.0, 1.0]]], w = [[1.0, 2.0], [0.0, 1.0]], keys = [[[1.0, 1.0]]]
Output: [[[3.00000],[1.00000]]]
```

**Example 2**
```text
Input: q = [[[1.0, 2.0]], [[3.0, 0.0]]], w = [[1.0, 0.0], [0.0, 1.0]], keys = [[[1.0, 1.0], [0.0, 1.0]], [[2.0, 0.0], [1.0, 5.0]]]
Output: [[[3.00000,2.00000]],[[6.00000,3.00000]]]
```

## Constraints

- `1 <= B <= 64`
- `1 <= n, m <= 256`
- `1 <= d <= 128`
