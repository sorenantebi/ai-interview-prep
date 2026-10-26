---
topic: "NumPy"
difficulty: Medium
---
# IoU Matrix - Solution

## Intuition

The overlap of two axis-aligned boxes is itself a box: its left edge is the larger of the two left edges, its right edge the smaller right edge, and likewise vertically. Broadcasting `a[:, None]` against `b[None, :]` computes these edges for all `n·m` pairs at once.

## Approach

1. Compute both box areas.
2. Intersection corners: `max` of the `x1`/`y1` columns and `min` of the `x2`/`y2` columns, broadcast to `(n, m)`.
3. Intersection width and height are clipped at `0` (no overlap); multiply them for the intersection area.
4. `union = area_a[:, None] + area_b[None, :] - inter`; divide where `union > 0`, else `0`.

## Code

```python
import numpy as np

def iou_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    x1 = np.maximum(a[:, None, 0], b[None, :, 0])
    y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    x2 = np.minimum(a[:, None, 2], b[None, :, 2])
    y2 = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    union = area_a[:, None] + area_b[None, :] - inter
    return np.divide(inter, union, out=np.zeros_like(inter, dtype=float), where=union > 0)
```

## Complexity

- **Time:** `O(n·m)`
- **Space:** `O(n·m)`
