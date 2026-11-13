# Learn: Range Grid

## The idea

- The task: make a run of consecutive whole numbers, then lay it out as a table with a set number of rows.
- You choose the rows; NumPy works out the columns.
- **Where it shows up:** data and ML code constantly turns flat values into tables.
  - A flat list of values becomes a batch (rows = samples).
  - Flat pixels become an image (rows = pixel lines).
  - A flat vector becomes a grid of features.
- **Array**: NumPy's fixed-size, typed table of numbers.
  - A 1-D array is a flat row of values.
  - A 2-D array has rows and columns.
- **Shape**: a tuple with the size of each dimension.
  - `(2, 3)` means 2 rows and 3 columns.
- **Reshape**: view the same numbers with a different shape.
  - The total number of elements must stay the same.
- **Row-major order**: values fill the first row left to right, then the second row, and so on.
- **`-1` in reshape**: "work out this size for me".
  - NumPy divides the total element count by the other sizes you gave.

## Work it by hand

Example 1: `start = 0`, `stop = 6`, `rows = 2`.

1. Make the flat run from `start` up to, but not including, `stop`.
   - Values: `[0, 1, 2, 3, 4, 5]`, shape `(6,)`.
2. You want 2 rows and don't know the columns, so the target shape is `(2, -1)`.
3. NumPy infers the columns: 6 elements / 2 rows = 3. Shape `(2, 3)`.
4. Fill row by row.
   - Row 0 takes the first 3 values: `0, 1, 2`.
   - Row 1 takes the next 3 values: `3, 4, 5`.

| Step | Value | Shape |
|---|---|---|
| flat array | `[0 1 2 3 4 5]` | `(6,)` |
| after reshape | `[[0 1 2] [3 4 5]]` | `(2, 3)` |

- Final answer: `[[0,1,2],[3,4,5]]`.

## Tools you'll need

### np.arange(start, stop)

- Returns a 1-D array of integers from `start` up to but **not including** `stop`, stepping by 1.
- With one argument, `np.arange(n)`, it starts at 0.

```python
import numpy as np

a = np.arange(10, 15)
print(a)        # [10 11 12 13 14]
print(a.shape)  # (5,)
print(np.arange(4))  # [0 1 2 3]
```

### arr.reshape(new_shape)

- Gives the same data a new shape, filled in row-major order.
- The product of the new sizes must equal the number of elements.
- It returns the reshaped array and leaves the original's shape alone.

```python
import numpy as np

a = np.arange(8)
b = a.reshape(4, 2)
print(b.tolist())  # [[0, 1], [2, 3], [4, 5], [6, 7]]
print(b.shape)     # (4, 2)
print(a.shape)     # (8,)
```

### -1 as a size in reshape

- At most one dimension can be `-1`.
- NumPy computes it as total elements divided by the product of the other sizes.
- It works in either position.

```python
import numpy as np

a = np.arange(12)
print(a.reshape(3, -1).shape)  # (3, 4)
print(a.reshape(-1, 6).shape)  # (2, 6)
print(a.reshape(-1).shape)     # (12,)
```

### arr.shape and arr.size

- `shape` is the tuple of dimension sizes.
- `size` is the total number of elements.
- Together they let you check that a reshape did what you expected.

```python
import numpy as np

a = np.arange(20).reshape(4, -1)
print(a.shape)  # (4, 5)
print(a.size)   # 20
```

## Common mistakes

- **Off-by-one on `stop`.** `np.arange(start, stop)` excludes `stop`.
  - Don't add 1 to it. Example 1 has `stop = 6` and ends at 5.
- **Swapping rows and columns.** `rows` is the given number, so it goes first and `-1` goes second.
  - Putting `-1` first would fix the columns and infer the rows instead.
- **Expecting column-by-column filling.** Reshape fills row by row.
  - The first block of values all lands in row 0, not down the first column.
- **Returning a flat array.** The result must be 2-D, even for a single column like `[[3],[4],[5],[6]]`.
  - Check that the shape has two entries.
- **Worrying about sizes that don't divide.** `reshape` raises an error if the numbers don't fit.
  - The problem guarantees `(stop - start) % rows == 0`, so you don't need to handle it.

## Hints

### Hint 1
- Build the flat run of consecutive integers from `start` up to, but not including, `stop`.
- Rearrange that run into a table with `rows` rows.
- Let NumPy decide how many columns are needed.

### Hint 2
- Use `np.arange` for the flat array; its shape is `(stop - start,)`.
- Call `.reshape` on it with two sizes to get shape `(rows, cols)`.
- For the second size, use `-1`.

### Hint 3
- The target shape is "`rows` rows, and however many columns fit".
- NumPy calculates the columns as `stop - start` divided by `rows`.
- Write `rows` first and `-1` second in the shape.
- Values fill row by row: row 0 gets the first block of numbers, row 1 the next block, and so on.
