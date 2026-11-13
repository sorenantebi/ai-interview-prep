# Learn: IoU Matrix

## The idea

- **IoU (intersection over union)** measures how much two rectangles overlap: shared area divided by total covered area.
  - Identical boxes give 1.
  - Boxes that don't overlap (or only touch) give 0.
- The task is to compute IoU for every pair: each box in `a` against each box in `b`.
  - The result has `n` rows and `m` columns.
  - Entry `[i, j]` compares `a[i]` with `b[j]`.
- In ML, this is core to object detection.
  - Evaluation reports match predicted boxes to ground-truth boxes with IoU.
  - Training pipelines use it to assign anchors and to remove duplicate detections.
- **Broadcasting**: when you combine arrays of different shapes, NumPy stretches size-1 axes to match.
  - A `(n, 1)` array combined with a `(1, m)` array gives an `(n, m)` result, one value per pair.
- **`None` / `np.newaxis`**: putting it in an index inserts a size-1 axis there.
- **Intersection box**: the overlap of two axis-aligned boxes is itself a box.
  - Its left edge is the larger of the two left edges; its right edge is the smaller of the two right edges.
  - The same holds vertically for top and bottom.
  - If its width or height would be negative, the boxes don't overlap.
- **Union**: area of the first box plus area of the second box minus the intersection (so the overlap isn't counted twice).

## Work it by hand

Example 1: `a = [[0, 0, 2, 2]]`, `b = [[1, 1, 3, 3], [5, 5, 6, 6]]`, so n = 1, m = 2.

1. **Areas** (width * height):

   | box | width | height | area |
   |---|---|---|---|
   | a[0] | 2 | 2 | 4 |
   | b[0] | 2 | 2 | 4 |
   | b[1] | 1 | 1 | 1 |

2. **Overlap edges per pair** (each edge array has shape `(1, 2)`):

   | pair | left = max(x1s) | top = max(y1s) | right = min(x2s) | bottom = min(y2s) |
   |---|---|---|---|---|
   | a[0], b[0] | max(0,1) = 1 | 1 | min(2,3) = 2 | 2 |
   | a[0], b[1] | max(0,5) = 5 | 5 | min(2,6) = 2 | 2 |

3. **Overlap width and height, negatives set to 0:**
   - Pair (0,0): width 2-1 = 1, height 1, so intersection = 1.
   - Pair (0,1): width 2-5 = -3 becomes 0, height -3 becomes 0, so intersection = 0.
   - Intersections: `[[1, 0]]`.

4. **Union = area_a + area_b - intersection:**
   - Pair (0,0): 4 + 4 - 1 = 7.
   - Pair (0,1): 4 + 1 - 0 = 5.

5. **Divide:** 1/7 = 0.14286 and 0/5 = 0.
   - Result: `[[0.14286, 0.00000]]`, which matches the expected output.

## Tools you'll need

### Column indexing `r[:, k]`

- Picks column `k` from every row.
- A `(n, 4)` array gives a `(n,)` array.

```python
import numpy as np
r = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(r[:, 2])  # [ 3  7 11]
print(r[:, 2].shape)  # (3,)
```

### `None` / `np.newaxis` (adding an axis)

- Inserts a size-1 axis at that position.
- Turns a flat vector into a column or a row so broadcasting can pair things up.

```python
import numpy as np
v = np.array([10, 20, 30])
print(v[:, None].shape)  # (3, 1)
print(v[None, :].shape)  # (1, 3)
```

### Broadcasting

- A `(n, 1)` array and a `(1, m)` array combine into `(n, m)`.
- Each cell pairs one element from each side.

```python
import numpy as np
p = np.array([1, 2, 3])
q = np.array([10, 20])
t = p[:, None] + q[None, :]
print(t)  # [[11 21]
          #  [12 22]
          #  [13 23]]
print(t.shape)  # (3, 2)
```

### `np.maximum(x, y)` and `np.minimum(x, y)`

- Compare two arrays element by element and keep the larger (or smaller) value.
- They broadcast.
- Don't confuse them with `np.max`, which reduces one array along an axis.

```python
import numpy as np
print(np.maximum(np.array([1, 5, 2]), np.array([3, 3, 3])))  # [3 5 3]
print(np.minimum(np.array([[1], [9]]), np.array([[4, 0]])))  # [[1 0]
                                                              #  [4 0]]
```

### `np.clip(x, lo, hi)`

- Limits values to the range `[lo, hi]`.
- Pass `None` for a side you don't want to limit.

```python
import numpy as np
w = np.array([-2.0, 0.5, 3.0])
print(np.clip(w, 0, None))  # [0.  0.5 3. ]
```

### `np.divide(x, y, out=..., where=...)`

- Plain division by 0 gives `nan` or `inf` plus a warning.
- With `where=cond`, NumPy divides only where `cond` is True and leaves other positions as they are in `out`.
- So start `out` as zeros.

```python
import numpy as np
x = np.array([1.0, 2.0, 3.0])
y = np.array([2.0, 0.0, 4.0])
out = np.zeros_like(x)
print(np.divide(x, y, out=out, where=y > 0))  # [0.5  0.   0.75]
```

## Common mistakes

- **Forgetting to clip.** Two boxes far apart give a negative width and a negative height, and their product is positive, a fake overlap.
  - Clip each side at 0 *before* multiplying.
- **Mixing up `np.maximum` and `np.max`.** You need the element-wise version to compare `a` against `b`.
  - `np.max` collapses an axis and gives the wrong shape.
- **Wrong broadcast axes.** `a` goes on axis 0 as `(n, 1)`, `b` on axis 1 as `(1, m)`.
  - Swapped, you get an `(m, n)` result, or a shape error when `n != m`.
- **Dividing by a zero union.** Two zero-area boxes give union 0, and plain `/` gives `nan`.
  - Divide only where the union is positive, and leave 0 elsewhere.
- **Integer inputs.** With integer arrays, make sure the final result is a float array, not truncated.

## Hints

### Hint 1
- Compute the area of every box in `a` and in `b`.
- For every pair, find the overlap rectangle's left and top edges, and its right and bottom edges.
- Turn those into an overlap width and height, never below 0, then an intersection area.
- Get the union from the two areas and the intersection.
- Divide, making sure a union of 0 gives 0.

### Hint 2
- Areas: column indexing, so `a[:, 2] - a[:, 0]` has shape `(n,)`.
- Pairwise edges: `np.maximum` / `np.minimum` on `a[:, None, k]` (shape `(n, 1)`) and `b[None, :, k]` (shape `(1, m)`), giving `(n, m)` for each of the four edges.
- Widths and heights: subtract the edges and clip at 0, still `(n, m)`.
- Intersection: multiply width by height, shape `(n, m)`.
- Union: make the areas broadcastable with `[:, None]` and `[None, :]`, giving `(n, m)`.
- Final division: `np.divide` with `out` and `where`, shape `(n, m)`.

### Hint 3
- Left edge = larger of the two x1 values; top edge = larger of the two y1 values.
- Right edge = smaller of the two x2 values; bottom edge = smaller of the two y2 values.
- Width = right - left and height = bottom - top, each clipped to at least 0.
- Intersection = width * height.
- Union = area_a (as a column) + area_b (as a row) - intersection.
- Divide intersection by union only where union > 0, and leave 0 elsewhere.
