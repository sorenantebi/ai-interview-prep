# Learn: Batched Bilinear Scores

## The idea

- **Bilinear score**: a number saying how well a query vector fits a key vector, with a weight matrix `w` in between.
  - Plain dot product: `q · k`.
  - Bilinear: `q · (w @ k)`, so the key is transformed by `w` first.
- The matrix `w` lets a model learn which parts of `q` should match which parts of `k`.
- It shows up in "general" (bilinear) attention layers and in recommender and retrieval models that score query-item pairs.
- **Batch**: a stack of `B` independent examples stored as one array with an extra leading axis.
- Looping over the batch in Python is slow, so the goal is one NumPy expression for all `B·n·m` scores.
- **`@`**: matrix multiplication.
  - With more than two axes, it treats the last two as the matrix and all earlier axes as batch axes.
- **Broadcasting**: NumPy reuses an array across a missing axis.
  - Here a 2-D `w` is reused for every batch element without copying.
- The real task is arranging shapes so the inner sizes line up: `(n, d) @ (d, m)` gives `(n, m)`.

## Work it by hand

Example 1: `B = 1`, `n = 2`, `m = 1`, `d = 2`.

- `q[0] = [[1, 0], [0, 1]]`, shape `(2, 2)`
- `w = [[1, 2], [0, 1]]`, shape `(2, 2)`
- `keys[0] = [[1, 1]]`, shape `(1, 2)`

1. Transform the one key `k = [1, 1]` with `w`:
   - row 1 of `w` is `[1, 2]`, so `1·1 + 2·1 = 3`
   - row 2 of `w` is `[0, 1]`, so `0·1 + 1·1 = 1`
   - `w @ k = [3, 1]`
2. Dot each query with `[3, 1]`:
   - `q[0] = [1, 0]`: `1·3 + 0·1 = 3`
   - `q[1] = [0, 1]`: `0·3 + 1·1 = 1`
3. Collect the results: 2 queries and 1 key give shape `(1, 2, 1)`.

```text
[[[3.0], [1.0]]]
```

- This matches the expected output.
- The same work by shape: `(2, 2) @ (2, 2) @ (2, 1)` gives `(2, 1)`.
  - `keys[b].T` has the keys as columns, so each output column is one key's scores.

## Tools you'll need

### `@` with batch axes

- Multiplies the last two axes as matrices and matches the leading axes.
- Inner sizes must agree: `(..., a, b) @ (..., b, c)` gives `(..., a, c)`.

```python
import numpy as np

x = np.ones((4, 2, 3))
y = np.ones((4, 3, 5))
print((x @ y).shape)  # (4, 2, 5)
```

### Broadcasting a 2-D matrix over a batch

- If one side is 2-D, NumPy reuses it for every batch element.

```python
import numpy as np

x = np.arange(12).reshape(2, 2, 3)
m = np.eye(3)
print((x @ m).shape)  # (2, 2, 3)
print(np.array_equal(x @ m, x))  # True
```

### `.transpose(axes)` / `np.swapaxes(a, i, j)`

- `transpose` takes the new order of all axes; `swapaxes` swaps just two.
- Plain `.T` reverses all axes, which is rarely what you want for batched data.

```python
import numpy as np

a = np.zeros((2, 3, 4))
print(a.transpose(0, 2, 1).shape)  # (2, 4, 3)
print(np.swapaxes(a, 1, 2).shape)  # (2, 4, 3)
print(a.T.shape)  # (4, 3, 2)
```

### `.shape`

- Your best debugging tool: print it after each step and compare with what you expect.

```python
import numpy as np

a = np.zeros((5, 3))
b = np.zeros((3, 7))
print((a @ b).shape)  # (5, 7)
```

## Common mistakes

- **Using `.T` on a 3-D array.** It reverses all three axes, giving `(d, m, B)`.
  - Use `transpose(0, 2, 1)` or `np.swapaxes` instead.
- **Transposing the wrong operand.** Only the keys need their last two axes swapped, not `q` or `w`.
  - Check that inner sizes match: `(n, d) @ (d, m)`.
- **Applying `w` on the wrong side.** `q @ w` differs from `w @ q` unless `w` is symmetric.
  - Follow the order in the formula.
- **Reaching for `np.einsum`.** The hidden tests reject it; use `@`.
- **Looping over `B` in Python.** It works but misses the point; let `@` handle the batch axis.

## Hints

### Hint 1
- Apply the weight matrix to the queries first, giving a batch of `(n, d)` arrays.
- Swap the last two axes of the keys, so each batch element is a normal `(d, m)` matrix.
- Multiply the two results.

### Hint 2
- `q @ w`: `w` is broadcast over the batch, giving shape `(B, n, d)`.
- Swap the last two axes of `keys` with `transpose` or `swapaxes`: shape `(B, d, m)`.
- Multiply the two with `@`: shape `(B, n, m)`.

### Hint 3
- For each batch element `b`, `s[b, i, j]` is row `i` of `q[b] @ w` dotted with row `j` of `keys[b]`.
- Swapping the last two axes of `keys` turns "row `j` of `keys[b]`" into "column `j`", which is what a matrix product multiplies against.
- So the answer is the transformed queries times the transposed keys, in that order.
