# Learn: K-Means

## The idea

- **K-means** groups points into `k` clusters, where each cluster is described by one point: its centroid.
- **Centroid**: the average position of a cluster's members.
- The task: start from `k` given centroids, then repeat two steps `iterations` times.
  - Assign every point to its nearest centroid.
  - Move each centroid to the average of the points it just received.
- It shows up in customer segmentation, colour compression in images, building a "vocabulary" of vectors, and quick first looks at unlabelled data.
- **Lloyd's algorithm**: the name of this assign-then-update loop.
  - The starting centroids are given, so the result is fully predictable.
- **Euclidean distance**: the straight-line distance between two points.
  - Squared distances pick the same nearest centroid, so you can skip the square root.
- **Broadcasting**: NumPy stretches size-1 axes so arrays of different shapes can be combined.
  - It lets you get all point-to-centroid differences without a Python loop.
- **Label**: the index of the centroid a point belongs to.
- **Empty cluster**: a centroid that receives no points. It stays where it is.

## Work it by hand

Example 1: four points, two centroids, one iteration.

```text
X  = (0,0) (0,1) (10,10) (10,11)      shape (4, 2)
C0 = (0,0)   C1 = (10,10)             shape (2, 2)
```

1. **Squared distances**, one row per point, one column per centroid (shape `(4, 2)`):

| point | to C0 | to C1 | nearest |
|---|---|---|---|
| (0,0) | 0 | 200 | 0 |
| (0,1) | 1 | 181 | 0 |
| (10,10) | 200 | 0 | 1 |
| (10,11) | 221 | 1 | 1 |

2. **Labels**: `[0, 0, 1, 1]`, shape `(4,)`.
3. **Update cluster 0**: members (0,0) and (0,1), mean = (0, 0.5).
4. **Update cluster 1**: members (10,10) and (10,11), mean = (10, 10.5).
5. **Result**: centroids `[[0, 0.5], [10, 10.5]]`, labels `[0, 0, 1, 1]`, matching the expected output.

- Example 2 shows the empty-cluster rule: the centroid at 100 gets no points, so it stays at 100.

## Tools you'll need

### Broadcasting with `None` / `np.newaxis`
- Indexing with `None` inserts a new axis of size 1.
- To compare every row of `A` with every row of `B`, give `A` shape `(n, 1, d)` and `B` shape `(1, k, d)`.
  - Subtracting gives shape `(n, k, d)`.

```python
import numpy as np
A = np.array([[1, 2], [3, 4], [5, 6]])   # 3 points
B = np.array([[0, 0], [1, 1]])           # 2 references
diff = A[:, None, :] - B[None, :, :]
print(diff.shape)  # (3, 2, 2)
print(diff[2, 1])  # [4 5]
```

### `arr.sum(axis=...)`
- Adds values along one axis, and that axis disappears from the shape.
- Summing the last axis collapses the coordinates into one number per pair.

```python
import numpy as np
a = np.arange(12).reshape(3, 2, 2)
print((a ** 2).sum(axis=2).shape)  # (3, 2)
print((a ** 2).sum(axis=2))
# [[  1  13]
#  [ 41  85]
#  [145 221]]
```

### `np.argmin(arr, axis=1)`
- Returns the index of the smallest value along an axis.
- On ties it returns the **first** one, which is exactly the smallest-index rule the problem asks for.

```python
import numpy as np
m = np.array([[3, 1, 1], [0, 5, 2]])
print(m.argmin(axis=1))  # [1 0]
```

### Boolean masks
- Comparing an array to a value gives a True/False array.
- Using it as a row index keeps only the matching rows; no match gives zero rows.

```python
import numpy as np
P = np.array([[1., 2.], [3., 4.], [5., 6.]])
lab = np.array([1, 0, 1])
print(lab == 1)            # [ True False  True]
print(P[lab == 1])
# [[1. 2.]
#  [5. 6.]]
print(P[lab == 7].shape)   # (0, 2)
```

### `arr.mean(axis=0)` and `len(...)`
- `mean(axis=0)` averages down the rows and gives one value per column.
- On an empty array it returns NaN with a warning, so check the count first with `len`.

```python
import numpy as np
Q = np.array([[2., 4.], [4., 8.]])
print(Q.mean(axis=0))  # [3. 6.]
print(len(Q[:0]))      # 0
```

### `np.array(x, dtype=float)`
- Makes a new float copy, so your input stays untouched.
- Float storage can hold means like 0.5, which an integer array cannot.

```python
import numpy as np
c = np.array([[1, 2]])
f = np.array(c, dtype=float)
f[0, 0] = 1.5
print(c[0, 0], f[0, 0])  # 1 1.5
```

## Common mistakes

- **Wrong axis in `sum` or `argmin`.**
  - The distance matrix is `(n, k)`: sum over the coordinate axis (last), then `argmin` over the centroid axis (axis 1).
  - Print shapes after each step.
- **Integer centroids.**
  - Writing 0.5 into an int array silently truncates it.
  - Copy with `dtype=float` first.
- **Empty clusters give NaN.**
  - Averaging zero points produces NaN.
  - Skip the update when a cluster has no members.
- **Changing the caller's array.**
  - Updating `centroids` in place alters the input.
  - Work on a copy.
- **Returning stale labels.**
  - Labels must come from the last assign step, centroids from the last update.
  - Keep both in variables that survive the loop.

## Hints

### Hint 1
- Repeat `iterations` times.
- Compute the distance from every point to every centroid.
- Pick the nearest centroid for each point.
- For each centroid, average its assigned points; leave it alone if it has none.
- After the loop, return the centroids and the last labels.

### Hint 2
- Give `X` a new middle axis and the centroids a new first axis, subtract, square, and sum over the last axis: shape `(n, k)`.
- `argmin` along axis 1 gives labels of shape `(n,)`.
- For the update, loop over the `k` centroids (not the points).
  - Select rows with a boolean mask on the labels.
  - `mean(axis=0)` gives shape `(d,)`.

### Hint 3
- For cluster `j`, the members are the rows of `X` where `labels == j`.
- If there is at least one member, the new centroid `j` is the column-wise sum of those rows divided by their count.
- If there are none, keep the old row.
- Ties need no extra code, because `argmin` returns the lowest index.
