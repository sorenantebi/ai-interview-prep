---
topic: "NumPy"
difficulty: Hard
---
# Non-Maximum Suppression

**Topic:** NumPy · **Difficulty:** Hard

## Problem

Object detectors output many overlapping boxes for the same object. Non-maximum suppression keeps the best one of each cluster. Given boxes of shape `(n, 4)` as `[x1, y1, x2, y2]` (continuous coordinates, area `(x2 - x1) * (y2 - y1)`), their `scores` of shape `(n,)` and an `iou_threshold`, run greedy NMS:

1. Order the boxes by score, highest first; equal scores keep the lower index first.
2. Take the first remaining box and keep it.
3. Remove every remaining box whose IoU with it is **strictly greater** than `iou_threshold`.
4. Repeat until no boxes remain.

Return the kept indices as a 1-D integer array, in the order they were kept. IoU is `0` when the union area is `0`. A loop over kept boxes is expected, but compare each kept box with all remaining boxes in one vectorised step.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: boxes = [[0.0, 0.0, 2.0, 2.0], [0.1, 0.0, 2.0, 2.0], [3.0, 3.0, 4.0, 4.0]], scores = [0.9, 0.8, 0.7], iou_threshold = 0.5
Output: [0,2]
```

**Example 2**
```text
Input: boxes = [[0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0], [0.5, 0.0, 1.5, 1.0]], scores = [0.5, 0.5, 0.9], iou_threshold = 0.3
Output: [2]
```

## Constraints

- `0 <= n <= 5000`
- `0 <= iou_threshold <= 1`
- `0 <= x1 <= x2`, `0 <= y1 <= y2`
