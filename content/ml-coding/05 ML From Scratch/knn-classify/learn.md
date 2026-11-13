# Learn: K-Nearest Neighbours Classifier

## The idea

- **K-nearest neighbours (KNN)**: classify a new point by finding the `k` labelled training points closest to it and letting them vote.
  - The most common label among those `k` neighbours wins.
  - Think of asking your `k` closest neighbours which party they support and going with the majority.
- There is no training step; the "model" is just the stored training data.
- It shows up as a simple baseline in evaluation reports.
- It is also used in feature pipelines to check whether embeddings of similar items land close together.
- **Euclidean distance**: the straight-line distance between two points.
  - For points `a` and `b` it is `sqrt(sum((a - b)^2))`.
  - Squared distances sort in the same order, so you can skip the square root.
- **Broadcasting**: NumPy stretches arrays of different shapes so they can be combined elementwise.
  - A `(q, 1, d)` array minus a `(1, m, d)` array gives `(q, m, d)`.
- **Stable sort**: a sort that keeps equal elements in their original order.
  - This is how the "smaller index counts as closer" rule can be met.
- Two tie rules matter here:
  - Equal distances: the smaller training index is closer.
  - Equal votes: the smallest label wins.

## Work it by hand

Example 1: `A=(0,0)` label 0, `B=(1,0)` label 0, `C=(5,5)` label 1, `D=(6,5)` label 1, with `k = 3`.

1. **Test point 1: (0.5, 0.5).** Squared distances to A, B, C, D:

   | Train point | Calculation | Squared distance |
   |---|---|---|
   | A (index 0) | 0.5² + 0.5² | 0.5 |
   | B (index 1) | 0.5² + 0.5² | 0.5 |
   | C (index 2) | 4.5² + 4.5² | 40.5 |
   | D (index 3) | 5.5² + 4.5² | 50.5 |

2. Sort: A, B (tied, A first by index), C, D. The 3 nearest are A, B, C with labels `[0, 0, 1]`.
3. Votes: label 0 has 2, label 1 has 1. Prediction **0**.
4. **Test point 2: (5.5, 4.0).** Squared distances:

   | Train point | Calculation | Squared distance |
   |---|---|---|
   | A | 5.5² + 4² | 46.25 |
   | B | 4.5² + 4² | 36.25 |
   | C | 0.5² + 1² | 1.25 |
   | D | 0.5² + 1² | 1.25 |

5. Sort: C, D (tied, C first), B, A. The 3 nearest are C, D, B with labels `[1, 1, 0]`.
6. Votes: label 1 has 2, label 0 has 1. Prediction **1**.
7. Result: `[0, 1]`, which matches the expected output.
8. Shapes for the whole example:
   - distance matrix: `(2, 4)`
   - neighbour indices: `(2, 3)`
   - predictions: `(2,)`

## Tools you'll need

### Broadcasting with `None` (`np.newaxis`)

- Indexing with `None` inserts a length-1 axis.
- A `(2, 1)` array minus a `(1, 3)` array gives every pairwise difference as `(2, 3)`.

```python
import numpy as np
a = np.array([10, 20])
b = np.array([1, 2, 3])
diff = a[:, None] - b[None, :]
print(diff.shape)  # (2, 3)
print(diff)  # [[ 9  8  7]
             #  [19 18 17]]
```

### `arr.sum(axis=...)`

- Adds along one axis and removes it.
- For distances you sum over the feature axis `d`.

```python
import numpy as np
a = np.arange(24).reshape(2, 3, 4)
print(a.sum(axis=2).shape)  # (2, 3)
print(a.sum(axis=0).shape)  # (3, 4)
```

### `np.argsort(a, axis=1, kind="stable")`

- Returns the indices that would sort each row, not the sorted values.
- `kind="stable"` keeps equal values in their original order.

```python
import numpy as np
a = np.array([[3, 1, 3, 2]])
print(np.argsort(a, axis=1, kind="stable"))  # [[1 3 0 2]]
```

- The two 3s keep their order: index 0 comes before index 2.

### Slicing the first `k` columns: `idx[:, :k]`

- Keeps all rows and only the first `k` columns.
- The shape goes from `(q, m)` to `(q, k)`.

```python
import numpy as np
idx = np.array([[4, 2, 0, 1], [3, 1, 2, 0]])
print(idx[:, :2])  # [[4 2]
                   #  [3 1]]
```

### Fancy indexing: `labels[idx]`

- Indexing with an integer array looks up many values at once.
- The result has the shape of the index array.

```python
import numpy as np
labels = np.array([7, 8, 9])
idx = np.array([[2, 0], [1, 1]])
print(labels[idx])  # [[9 7]
                    #  [8 8]]
```

### `np.bincount(a)` and `argmax()`

- `bincount` counts how often each non-negative integer appears: position `v` holds the count of `v`.
- `argmax` returns the position of the first maximum, so ties go to the smallest value.

```python
import numpy as np
counts = np.bincount(np.array([2, 0, 2, 0, 3]))
print(counts)  # [2 0 2 1]
print(counts.argmax())  # 0
```

## Common mistakes

- **Summing over the wrong axis.**
  - The distance sum must be over the feature axis (the last one), leaving `(q, m)`.
  - Print the shape to check.
- **Unstable sorting.**
  - The default `argsort` does not promise to keep equal distances in index order.
  - Pass `kind="stable"`.
- **Worrying about `sqrt`.**
  - You don't need it; squared distances sort the same way.
  - Skipping it also avoids tiny rounding differences.
- **Breaking vote ties wrongly.**
  - Something like `max(set(labels), key=labels.count)` can pick any tied label.
  - `bincount(...).argmax()` gives the smallest one.
- **Sorting the wrong axis.**
  - Sort each test row across the `m` training points (`axis=1`), not down the columns.

## Hints

### Hint 1

- Compute the distance from every test point to every training point.
- For each test point, pick the `k` closest training points, using index order to break ties.
- Look up the labels of those neighbours.
- Count the votes and choose the winner, using the smallest label to break ties.

### Hint 2

- Broadcast with `None` indexing and sum over the last axis: a `(q, m)` distance matrix.
- Stable `argsort` along axis 1, then slice the first `k` columns: `(q, k)` indices.
- Index `y_train` with those indices: a `(q, k)` array of labels.
- Apply `np.bincount` and `argmax` to each row: one label per test point, `(q,)` overall.

### Hint 3

- The difference array has shape `(q, m, d)`: test points on axis 0, training points on axis 1, features on axis 2.
- Square it and sum over axis 2 to get `(q, m)`.
- After the stable sort and slice, each row of the label array holds the `k` neighbour labels of one test point.
- For each row, the vote counts are `bincount(row)`, and the position of the largest count is the winning label.
- Collect one result per row into an integer array of length `q`.
