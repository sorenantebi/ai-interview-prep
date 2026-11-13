# Learn: Multiplication Table with Broadcasting

## The idea

- The task: build a 2-D grid where the cell in row `i`, column `j` is `(i + 1) * (j + 1)`.
  - Each cell is just its row number times its column number.
- You could fill it with two loops, but NumPy can do it in one operation.
- **Broadcasting**: when you combine arrays of different shapes, NumPy stretches the size-1 (or missing) dimensions to match the other array.
  - It does this without copying data.
  - A column of shape `(n, 1)` times a row of shape `(m,)` gives a grid of shape `(n, m)`.
- **Shape**: a tuple with the size of each dimension.
  - 4 numbers in a vector: `(4,)`.
  - 3 numbers as a column: `(3, 1)`.
- Where it shows up in ML and data work:
  - Subtracting the mean from every row of a dataset.
  - Scaling each feature column.
  - Adding a bias vector to a batch of outputs.
- Broadcasting replaces loops with one readable line, and it runs much faster.

## Work it by hand

Example 1: `n = 3`, `m = 4`.

1. Make the row numbers: `[1, 2, 3]`, shape `(3,)`.
2. Make the column numbers: `[1, 2, 3, 4]`, shape `(4,)`.
3. Turn the row numbers into a column, shape `(3, 1)`:

```text
[[1],
 [2],
 [3]]
```

4. Multiply. NumPy stretches the `(3, 1)` column across 4 columns, and the `(4,)` row down 3 rows. Both become `(3, 4)`:

```text
column stretched      row stretched
[[1, 1, 1, 1],        [[1, 2, 3, 4],
 [2, 2, 2, 2],         [1, 2, 3, 4],
 [3, 3, 3, 3]]         [1, 2, 3, 4]]
```

5. Multiply cell by cell:

```text
[[1*1, 1*2, 1*3, 1*4],     [[1, 2, 3,  4],
 [2*1, 2*2, 2*3, 2*4],  =   [2, 4, 6,  8],
 [3*1, 3*2, 3*3, 3*4]]      [3, 6, 9, 12]]
```

6. Result shape is `(3, 4)`, which matches the expected output.

## Tools you'll need

### np.arange(start, stop)

- Creates a 1-D array of evenly spaced integers from `start` up to, but **not including**, `stop`.
- With one argument, `np.arange(k)`, it starts at 0.

```python
import numpy as np

a = np.arange(5, 9)
print(a)        # [5 6 7 8]
print(a.shape)  # (4,)
```

### Adding an axis with `[:, None]`

- Indexing with `None` (same as `np.newaxis`) inserts a new dimension of size 1 at that position.
- `v[:, None]` turns shape `(k,)` into a column `(k, 1)`.
- `v[None, :]` turns it into a row `(1, k)`.

```python
import numpy as np

v = np.array([10, 20, 30])
print(v[:, None].shape)  # (3, 1)
print(v[None, :].shape)  # (1, 3)
print(v[:, None])
# [[10]
#  [20]
#  [30]]
```

### Broadcasting with `*`

- Arithmetic operators work element by element.
- When shapes differ, NumPy compares them from the right.
  - Two dimensions are compatible if they are equal or one of them is 1.
  - The size-1 dimension is stretched.
  - A missing dimension on the left counts as 1.

```python
import numpy as np

col = np.array([[1], [2]])    # shape (2, 1)
row = np.array([10, 20, 30])  # shape (3,)
out = col + row
print(out.shape)  # (2, 3)
print(out)
# [[11 21 31]
#  [12 22 32]]
```

### .shape

- Whenever broadcasting surprises you, print the shapes first.
- Shape `(3,)` and shape `(3, 1)` behave very differently.

```python
import numpy as np

a = np.arange(3)
print(a.shape)           # (3,)
print(a[:, None].shape)  # (3, 1)
print((a + a).shape)     # (3,)
```

## Common mistakes

- **Forgetting the new axis.** Multiplying two `(k,)` vectors gives another `(k,)` vector, not a grid.
  - Turn one of them into a column with `[:, None]`.
- **Putting the column on the wrong vector.** The column decides the number of rows.
  - If the `1..m` vector becomes the column, you get shape `(m, n)` instead of `(n, m)`.
- **Off-by-one with `arange`.** `np.arange(1, n)` stops at `n - 1`.
  - To include `n`, the stop value must be `n + 1`.
- **Starting at 0.** `np.arange(n)` gives `0..n-1`, but the table needs `1..n`.
  - Set the start to 1.
- **Reaching for loops.** The problem forbids them, and one broadcast multiplication is shorter and faster.

## Hints

### Hint 1
- Build a list of row numbers, from 1 up to `n`.
- Build a list of column numbers, from 1 up to `m`.
- Turn the row list into a column.
- Multiply the two together once.

### Hint 2
- `np.arange` makes each list, with shapes `(n,)` and `(m,)`.
- `[:, None]` turns the length-`n` list into a column of shape `(n, 1)`.
- Multiplying `(n, 1)` by `(m,)` broadcasts to shape `(n, m)`.

### Hint 3
- Both ranges start at 1 and include their upper limit, so the `stop` argument is the limit plus one.
- Put the new axis on the vector of length `n`.
- Then row `i` holds `(i + 1)` times the whole `1..m` list.
