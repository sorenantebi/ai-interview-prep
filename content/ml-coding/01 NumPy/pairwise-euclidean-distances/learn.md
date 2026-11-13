# Learn: Pairwise Euclidean Distances

## The idea

- The task: you have two piles of points, `a` with `n` points and `b` with `m` points, each point having `d` coordinates.
- You must measure the straight-line distance from every point in `a` to every point in `b`.
- The answer is an `(n, m)` table: entry `[i, j]` is the distance from `a[i]` to `b[j]`.
- It shows up in ML work such as:
  - k-nearest neighbours (distance from a query to every training point)
  - k-means (distance from each point to each centre)
  - embedding search and retrieval
  - kernel methods
- **Euclidean distance**: the ordinary ruler distance. Subtract coordinates, square the differences, add them up, take the square root.
- **Broadcasting**: NumPy's rule for combining arrays of different shapes. A dimension of size 1 is stretched to match the other array.
  - A `(n, 1)` array plus a `(1, m)` array gives an `(n, m)` array.
- **Squared-norm expansion**: squared distance = |x|² + |y|² − 2·x·y.
  - The first two terms depend on one point each, so they are vectors.
  - The cross term for all pairs is one matrix product.
- There are two loop-free routes:
  - Broadcast the differences into an `(n, m, d)` array: simple, but memory-hungry.
  - Use the expansion above: only `(n, m)` memory.
- **Why clip**: rounding can turn a true 0 into something like `-1e-13`, and the square root of that is `nan`.

## Work it by hand

Example 1: `a = [[0, 0], [3, 4]]` (shape `(2, 2)`), `b = [[0, 0]]` (shape `(1, 2)`). Use the expansion.

1. Squared norms of the rows of `a`: row 0 is 0²+0² = 0, row 1 is 3²+4² = 25.
   - As a column: `[[0], [25]]`, shape `(2, 1)`.
2. Squared norms of the rows of `b`: 0.
   - As a row: `[[0]]`, shape `(1, 1)`.
3. Dot products: `b.T` has shape `(2, 1)`, so the product has shape `(2, 1)`.
   - Row 0: 0·0 + 0·0 = 0. Row 1: 3·0 + 4·0 = 0.
   - Result: `[[0], [0]]`.
4. Combine: `[[0], [25]] + [[0]] - 2 * [[0], [0]]` = `[[0], [25]]`, shape `(2, 1)`.
5. Clip below at 0: nothing changes here.
6. Square root: `[[0], [5]]`.

Final output: `[[0.0], [5.0]]`, matching the expected `[[0.00000],[5.00000]]`.

## Tools you'll need

### arr.sum(axis=..., keepdims=...)

- Adds up entries along one axis. `axis=1` sums across columns, giving one value per row.
- `keepdims=True` keeps that axis with size 1, which is handy for broadcasting later.

```python
import numpy as np
x = np.array([[1., 2., 3.], [4., 5., 6.]])
print(x.sum(axis=1))  # [ 6. 15.]
print(x.sum(axis=1).shape)  # (2,)
print(x.sum(axis=1, keepdims=True).shape)  # (2, 1)
```

### Adding an axis with `[:, None]` / `[None, :]`

- `None` inserts a new axis of size 1.
- Use it to turn a flat vector into a column or a row.

```python
import numpy as np
v = np.array([10., 20., 30.])
print(v[:, None].shape)  # (3, 1)
print(v[None, :].shape)  # (1, 3)
```

### Broadcasting

- When shapes differ, size-1 dimensions are stretched.
- A column `(3, 1)` plus a row `(1, 2)` gives `(3, 2)`.

```python
import numpy as np
col = np.array([[1], [2], [3]])
row = np.array([[10, 20]])
print((col + row).shape)  # (3, 2)
print(col + row)
# [[11 21]
#  [12 22]
#  [13 23]]
```

### `@` and `.T`

- `@` is the matrix product: `(n, d) @ (d, m)` gives `(n, m)`.
- `.T` swaps the axes, so an `(m, d)` array becomes `(d, m)`.
- Entry `[i, j]` of `p @ q.T` is the dot product of row `i` of `p` with row `j` of `q`.

```python
import numpy as np
p = np.array([[1, 2], [3, 4], [5, 6]])
q = np.array([[1, 0], [0, 1]])
print((p @ q.T).shape)  # (3, 2)
print(p @ q.T)
# [[1 2]
#  [3 4]
#  [5 6]]
```

### np.maximum(x, 0)

- Compares element by element and keeps the larger value.
- With a scalar, it clips everything below that scalar.
- Not the same as `np.max`, which reduces to one value.

```python
import numpy as np
x = np.array([-1e-12, 2.0, -3.0])
print(np.maximum(x, 0.0))  # [0. 2. 0.]
```

### np.sqrt

- Element-wise square root.
- Negative input gives `nan` plus a warning, so clip first.

```python
import numpy as np
print(np.sqrt(np.array([4.0, 9.0, 0.0])))  # [2. 3. 0.]
```

## Common mistakes

- **Wrong shapes for the norms.** Two 1-D vectors of shapes `(n,)` and `(m,)` don't combine into `(n, m)`.
  - Make one a column `(n, 1)` and the other a row `(1, m)`.
- **Summing over the wrong axis.** Each row's squared norm needs `axis=1`, across the `d` coordinates.
  - `axis=0` sums over points instead.
- **Forgetting the clip.** Tiny negatives become `nan` under `np.sqrt`.
  - Clip to 0 first.
- **Using `*` instead of `@`.** `*` is element-wise.
  - The cross term needs the matrix product with `b` transposed.
- **Forgetting the factor 2.** The cross term is `2·a·b`, not `a·b`.

## Hints

### Hint 1

- Split the squared distance into three parts: one depending only on `a[i]`, one only on `b[j]`, and a mixed term.
- Compute each part for all rows at once.
- Add them into an `(n, m)` table.
- Fix tiny negatives.
- Take the square root.

### Hint 2

- Square and sum along the coordinate axis for each input: shapes `(n,)` and `(m,)`.
- Reshape them to `(n, 1)` and `(1, m)` with `None` indexing.
- Get the mixed term with a matrix product: shape `(n, m)`.
- Add everything together; broadcasting gives `(n, m)`.
- Clip with `np.maximum`, then apply `np.sqrt`.

### Hint 3

- For each pair: squared distance = (sum of squares of `a[i]`) + (sum of squares of `b[j]`) − 2 × (dot product of `a[i]` and `b[j]`).
- The dot products for all pairs form `a @ b.T`.
- Adding the column of `a` norms and the row of `b` norms to that matrix broadcasts to `(n, m)`.
- Replace any negative entry with 0.
- Take the square root of every entry.
