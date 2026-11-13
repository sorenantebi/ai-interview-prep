# Learn: Non-Maximum Suppression

## The idea

- **Non-maximum suppression (NMS)**: from a pile of overlapping boxes, keep the best-scoring one and drop its near-duplicates.
- An object detector (faces, cars, cells...) usually fires many times on the same object.
  - You get several slightly shifted boxes, each with a confidence score.
  - NMS runs after the model in almost every detection pipeline, and also inside evaluation code.
- **IoU (intersection over union)**: how much two boxes overlap.
  - The intersection is the area they share.
  - The union is the area covered by either box.
  - IoU = intersection / union. It is 0 for boxes that don't touch and 1 for identical boxes.
- **Greedy** rule: always take the best remaining box, never reconsider it.
  - Sort by score, keep the top box.
  - Delete every remaining box whose IoU with it is strictly above the threshold.
  - Repeat with whatever is left.
- **Broadcasting**: NumPy stretches a scalar or small array to match a bigger one.
  - It lets you compare one box against all remaining boxes in a single step, with no inner loop.
- **Queue**: here, the array of original indices still waiting to be processed, best score first.

## Work it by hand

Example 1: threshold 0.5, scores `[0.9, 0.8, 0.7]`.

- Boxes: A = `[0,0,2,2]`, B = `[0.1,0,2,2]`, C = `[3,3,4,4]`.
- Areas: A = 2·2 = 4, B = 1.9·2 = 3.8, C = 1·1 = 1.

1. Sort by score, highest first: queue = `[0, 1, 2]`.
2. Keep index 0 (A). Remaining: `[1, 2]`.
3. A vs B:
   - width = min(2,2) − max(0,0.1) = 1.9, height = 2, so intersection = 3.8.
   - union = 4 + 3.8 − 3.8 = 4, so IoU = 0.95.
4. A vs C:
   - width = min(2,4) − max(0,3) = −1. Negative means no overlap, so clip to 0.
   - intersection = 0, union = 4 + 1 − 0 = 5, so IoU = 0.
5. Remove boxes with IoU > 0.5: B goes (0.95), C stays (0). Queue: `[2]`.
6. Keep index 2 (C). The queue is empty, so stop.

Kept in order: `[0, 2]`.

| Step | queue | kept |
|---|---|---|
| start | `[0,1,2]` | `[]` |
| after A | `[2]` | `[0]` |
| after C | `[]` | `[0,2]` |

## Tools you'll need

### np.argsort(a, kind="stable")
- Returns the indices that would sort `a`, smallest first.
- For highest first, sort the negated array.
- `kind="stable"` keeps equal values in their original order, which gives the "lower index first" tie rule.

```python
import numpy as np
s = np.array([0.2, 0.9, 0.2, 0.5])
print(np.argsort(-s, kind="stable"))  # [1 3 0 2]
```

### Fancy indexing with an index array
- Indexing with an array of integers picks those rows, in that order.
- The result has one entry per index.

```python
import numpy as np
b = np.array([[1, 2], [3, 4], [5, 6]])
idx = np.array([2, 0])
print(b[idx])  # [[5 6]
               #  [1 2]]
print(b[idx, 1])  # [6 2]
print(b[idx].shape)  # (2, 2)
```

### Boolean masks
- A comparison gives an array of True/False.
- Using it as an index keeps only the True positions. This is how you drop elements.

```python
import numpy as np
v = np.array([10, 20, 30, 40])
m = np.array([0.1, 0.8, 0.3, 0.9]) <= 0.5
print(m)  # [ True False  True False]
print(v[m])  # [10 30]
```

### np.maximum / np.minimum (element-wise) with broadcasting
- Unlike `max`/`min`, these compare two arrays element by element.
- A scalar is stretched against an array.

```python
import numpy as np
a = np.array([1.0, 5.0, 3.0])
print(np.maximum(a, 2.0))  # [2. 5. 3.]
print(np.minimum(a, np.array([4.0, 4.0, 4.0])))  # [1. 4. 3.]
```

### np.clip(a, lo, hi)
- Limits values to a range. `None` means "no limit" on that side.
- Here it turns negative widths into 0.

```python
import numpy as np
w = np.array([-1.5, 0.0, 2.0])
print(np.clip(w, 0, None))  # [0. 0. 2.]
```

### Safe division with np.divide(..., out=, where=)
- Plain `/` gives `nan` or `inf` when dividing by 0.
- `np.divide` with `where=cond` divides only where `cond` is True and leaves `out` untouched elsewhere.

```python
import numpy as np
num = np.array([1.0, 2.0, 3.0])
den = np.array([2.0, 0.0, 4.0])
out = np.zeros(3)
print(np.divide(num, den, out=out, where=den > 0))  # [0.5  0.   0.75]
```

### Python list, np.array, and `.size`
- Collect kept indices in a list inside the loop, then convert at the end.
- `.size` is the element count, so `while arr.size:` loops until the array is empty.
- An empty list needs `dtype=int` to stay an integer array.

```python
import numpy as np
print(np.array([], dtype=int))  # []
print(np.array([], dtype=int).dtype)  # int64
print(np.arange(3).size)  # 3
```

## Common mistakes

- **Negative overlap not clipped.**
  - Boxes that don't touch give a negative width, and two negative sides multiply to a positive "area".
  - Clip width and height at 0 separately before multiplying.
- **Comparing against the wrong set.**
  - Compare the kept box only with boxes still in the queue, then rebuild the queue from the survivors.
  - Positions shift after filtering, so track original indices, not positions.
- **`>` vs `>=`.**
  - A box is removed only when IoU is strictly greater than the threshold.
  - Boxes with IoU equal to it survive.
- **Division by zero.**
  - Zero-area boxes can make the union 0.
  - IoU must be 0 there, not `nan`.
- **Ties and empty input.**
  - Use a stable sort so ties keep the lower index first.
  - With `n = 0`, return an empty integer array, not a float one.

## Hints

### Hint 1
- Precompute every box's area once.
- Sort the indices by score, ties by lower index. This is your queue.
- Loop while the queue is not empty:
  - Take the front of the queue and keep it.
  - Measure its overlap with every box behind it.
  - Keep in the queue only the boxes that are not too similar.
- Return the kept indices as an integer array.

### Hint 2
- `np.argsort(-scores, kind="stable")` gives the queue, shape `(n,)`.
- Inside the loop, split it into the front index and `rest`, shape `(m,)`.
- Fancy-index `boxes[rest]` to get shape `(m, 4)`.
- Compute intersection width, height and area, each of shape `(m,)`.
- Compute the union and the IoU, shape `(m,)`.
- A boolean mask on `rest` gives the new, shorter queue.

### Hint 3
- For kept box `i` and each box `j` in `rest`:
  - width = min(x2_i, x2_j) − max(x1_i, x1_j)
  - height = min(y2_i, y2_j) − max(y1_i, y1_j)
- Clip both at 0, then intersection = width · height.
- Union = area_i + area_j − intersection.
- IoU = intersection / union, set to 0 where the union is 0.
- The new queue is `rest` where IoU <= threshold.
- Finally, convert the kept list to an integer array.
