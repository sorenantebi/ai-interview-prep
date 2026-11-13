# Learn: Corners and Centre Row

## The idea

- **The task**: pick a few entries out of a 2-D array by position: the four corners and the middle row.
  - No loops and no maths are needed.
  - You only have to say *where* each value lives.
- **Indexing**: picking values by position.
  - In ML it shows up when you grab one sample from a batch, the last time step of a sequence, or one row of a feature matrix.
- **2-D array**: a grid with rows and columns.
  - Its `shape` is `(n, m)`: `n` rows, `m` columns.
- **Negative index**: counts from the end. `-1` is the last item, `-2` the one before it.
  - You never need to know how long the array is.
- **Floor division `//`**: divides and rounds down to a whole number.
  - `7 // 2` is `3` and `4 // 2` is `2`, so it gives a valid row number.

## Work it by hand

Example 1: `a` is a 3×3 grid, so `n = 3` and `m = 3`.

```text
        col 0  col 1  col 2
row 0     1.0    2.0    3.0
row 1     4.0    5.0    6.0
row 2     7.0    8.0    9.0
```

1. Top-left: row `0`, column `0`, value `1.0`.
2. Top-right: row `0`, column `-1` (which is column 2), value `3.0`.
3. Bottom-left: row `-1` (row 2), column `0`, value `7.0`.
4. Bottom-right: row `-1` (row 2), column `-1`, value `9.0`.
5. Put the four values in that order into one 1-D array of shape `(4,)`: `[1.0, 3.0, 7.0, 9.0]`.
6. Centre row number: `n // 2 = 3 // 2 = 1`.
7. Take row 1: `[4.0, 5.0, 6.0]`, shape `(3,)`.
8. Return both as a tuple:

```text
([1.0, 3.0, 7.0, 9.0], [4.0, 5.0, 6.0])
```

## Tools you'll need

### a[i, j]

- Picks one element: row `i`, column `j`.
- The result is a single number, not an array.

```python
import numpy as np

b = np.array([[10, 20, 30], [40, 50, 60]])
print(b[1, 2])  # 60
print(b[0, 1])  # 20
```

### Negative indices

- `-1` means "last", `-2` means "second to last".
- They work in each position separately.

```python
import numpy as np

b = np.array([[10, 20, 30], [40, 50, 60]])
print(b[-1, 0])   # 40
print(b[0, -2])   # 20
print(b[-1, -1])  # 60
```

### a[i] (a whole row)

- Giving only one index selects an entire row.
- The result is a 1-D array with `m` entries.

```python
import numpy as np

b = np.array([[1, 2], [3, 4], [5, 6]])
print(b[2])        # [5 6]
print(b[2].shape)  # (2,)
```

### a.shape and //

- `a.shape` is a tuple `(n, m)`, so `a.shape[0]` is the number of rows.
- Combine it with `//` to get a whole-number position.

```python
import numpy as np

b = np.zeros((5, 3))
print(b.shape)          # (5, 3)
print(b.shape[0] // 2)  # 2
print(6 // 2, 7 // 2)   # 3 3
```

### np.array([...])

- Builds a new array from a list of values.
- A list of three numbers gives a 1-D array of shape `(3,)`.

```python
import numpy as np

v = np.array([2.5, 7.0, 1.5])
print(v)        # [2.5 7.  1.5]
print(v.shape)  # (3,)
```

### Fancy indexing with index arrays

- Pass a list of row positions and a list of column positions.
  - NumPy pairs them up and returns one value per pair.
- It is an alternative to picking values one by one.

```python
import numpy as np

b = np.array([[1, 2, 3], [4, 5, 6]])
print(b[[0, 1], [2, 0]])  # [3 4]
```

## Common mistakes

- **Row and column swapped**: the first index is the row, the second the column.
  - Top-right is row `0`, column `-1`, not the other way round.
- **Using `n / 2` instead of `n // 2`**: single `/` gives a float like `1.5`, and NumPy rejects it as an index.
  - Use `//`.
- **Wrong centre for even `n`**: with `n = 4`, `n // 2 = 2` is the lower middle row, which is what the task wants.
  - Don't subtract 1.
- **Returning a list or four separate numbers**: `corners` must be one 1-D array of length 4.
  - The function returns a tuple of two things.
- **Mixing `a[0][0]` and `a[0, 0]`**: both work for single values, but the comma form is what this task practises.
  - Use one pair of brackets with a comma inside.

## Hints

### Hint 1
- Do two separate jobs: corners first, then the centre row.
- Collect the four corner values in the required order and store them as one 1-D array.
- Work out which row is in the centre and take it.
- Return both together as a tuple.

### Hint 2
- Corners: use `a[row, col]` with `0` and `-1` as positions, then wrap the four numbers in an array. Shape is `(4,)`.
- Row count: read `n` from `a.shape[0]`, then floor-divide by 2.
- Centre: use that number as a single row index. Shape is `(m,)`.

### Hint 3
- The corner order is: (first row, first column), (first row, last column), (last row, first column), (last row, last column).
  - In index terms, the first index is `0` or `-1` for the row, the second is `0` or `-1` for the column.
- The centre row number is `n // 2`, where `n` is the number of rows.
- Return the corners array and the centre row as a tuple, in that order.
