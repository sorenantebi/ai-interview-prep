---
topic: "NumPy"
difficulty: Hard
---
# Non-Maximum Suppression - Solution

## Intuition

Once boxes are sorted by score, the first remaining box can never be suppressed, because every box that could suppress it has a lower score and is removed or kept after it. So the greedy loop only needs, for each kept box, the IoU with all boxes still in the queue — one vectorised computation per kept box.

## Approach

1. `order = np.argsort(-scores, kind="stable")` sorts by score, ties by index.
2. While `order` is non-empty: keep `i = order[0]` and compute its IoU with the boxes `order[1:]` using broadcasting.
3. Continue with `order[1:][iou <= iou_threshold]`.
4. Return the kept indices as an integer array.

## Code

```python
import numpy as np

def nms(boxes: np.ndarray, scores: np.ndarray, iou_threshold: float) -> np.ndarray:
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    order = np.argsort(-scores, kind="stable")
    keep = []
    while order.size:
        i, rest = order[0], order[1:]
        keep.append(i)
        w = np.clip(np.minimum(boxes[i, 2], boxes[rest, 2]) - np.maximum(boxes[i, 0], boxes[rest, 0]), 0, None)
        h = np.clip(np.minimum(boxes[i, 3], boxes[rest, 3]) - np.maximum(boxes[i, 1], boxes[rest, 1]), 0, None)
        inter = w * h
        union = areas[i] + areas[rest] - inter
        iou = np.divide(inter, union, out=np.zeros_like(inter, dtype=float), where=union > 0)
        order = rest[iou <= iou_threshold]
    return np.array(keep, dtype=int)
```

## Complexity

- **Time:** `O(n·k) for k kept boxes, plus O(n log n) for the sort`
- **Space:** `O(n)`
