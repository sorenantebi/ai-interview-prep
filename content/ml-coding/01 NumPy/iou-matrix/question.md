---
topic: "NumPy"
difficulty: Medium
---
# IoU Matrix

**Topic:** NumPy · **Difficulty:** Medium

## Problem

Boxes are rows `[x1, y1, x2, y2]` with `x1 <= x2` and `y1 <= y2` in continuous coordinates, so a box's area is `(x2 - x1) * (y2 - y1)`. Given boxes `a` of shape `(n, 4)` and `b` of shape `(m, 4)`, return the `(n, m)` array whose entry `[i, j]` is the intersection over union (IoU) of `a[i]` and `b[j]`: the area of their overlap divided by the area of their union.

Boxes that only touch have IoU `0`. If the union area is `0` (both boxes have zero area), the IoU is `0`. No Python loops over boxes.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: a = [[0.0, 0.0, 2.0, 2.0]], b = [[1.0, 1.0, 3.0, 3.0], [5.0, 5.0, 6.0, 6.0]]
Output: [[0.14286,0.00000]]
```

**Example 2**
```text
Input: a = [[0.0, 0.0, 4.0, 4.0], [0.0, 0.0, 1.0, 1.0]], b = [[0.0, 0.0, 4.0, 4.0]]
Output: [[1.00000],[0.06250]]
```

## Constraints

- `1 <= n, m <= 2000`
- `0 <= x1 <= x2 <= 10^4`, `0 <= y1 <= y2 <= 10^4`
