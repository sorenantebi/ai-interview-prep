# Learn: One-Hot Encode

## The idea

- **One-hot encoding** turns a list of class numbers into a table of 0s and 1s.
  - Each class number becomes one row.
  - The row has a single `1` in the column matching the class, and `0` everywhere else.
  - With 3 classes, class `2` becomes `[0, 0, 1]`.
- The task: given `n` labels, build an `(n, num_classes)` integer array without looping over the labels.
- Why it's useful: models can't treat class numbers as quantities, since class `2` isn't "twice" class `1`.
  - One column per class removes that fake ordering.
- Where it shows up:
  - Feature pipelines, for categorical columns.
  - Training loops, for turning labels into target vectors for a loss.
- **Fancy indexing**: using an array of integers as an index, so NumPy picks many positions at once.
- **Shape**: the size along each axis.
  - Here the result has shape `(n, num_classes)`: one row per label, one column per class.

## Work it by hand

Example 1: `labels = [0, 2, 1]`, `num_classes = 3`.

1. Count the labels: `n = 3`, so the output shape is `(3, 3)`.
2. Start with all zeros:
   ```text
   [[0,0,0],
    [0,0,0],
    [0,0,0]]
   ```
3. Pair each row number with its label:

   | row i | labels[i] | cell to set |
   |-------|-----------|-------------|
   | 0     | 0         | (0, 0)      |
   | 1     | 2         | (1, 2)      |
   | 2     | 1         | (2, 1)      |

4. Put a `1` in each of those cells:
   ```text
   [[1,0,0],
    [0,0,1],
    [0,1,0]]
   ```
5. This matches the expected output.
   - The row numbers are `[0, 1, 2]`.
   - The column numbers are the labels `[0, 2, 1]`.
   - The two lists line up position by position.

## Tools you'll need

### np.zeros(shape, dtype=...)

- Creates an array filled with zeros; pass the shape as a tuple.
- The default dtype is float, so pass `dtype=int` for integers.

```python
import numpy as np

a = np.zeros((2, 4), dtype=int)
print(a.shape)  # (2, 4)
print(a)
# [[0 0 0 0]
#  [0 0 0 0]]
```

### np.arange(n)

- Returns the integers `0, 1, ..., n-1` as a 1-D array.
- Handy for "one index per row".
- With `n = 0` it returns an empty array.

```python
import numpy as np

print(np.arange(4))  # [0 1 2 3]
print(np.arange(0).shape)  # (0,)
```

### Fancy indexing with two index arrays

- Index a 2-D array with two integer arrays of the same length and NumPy pairs them up.
  - The first elements form one cell, the second elements form the next cell, and so on.
- The same works for assignment, in one statement with no loop.

```python
import numpy as np

m = np.zeros((3, 3), dtype=int)
rows = np.array([0, 1, 2])
cols = np.array([1, 1, 0])
m[rows, cols] = 5
print(m)
# [[0 5 0]
#  [0 5 0]
#  [5 0 0]]
```

- Cells chosen: `(0,1)`, `(1,1)`, `(2,0)`.

### len(a) and a.shape

- `len(a)` gives the size of the first axis; `a.shape` gives all sizes.
- Both work for empty arrays.

```python
import numpy as np

b = np.array([7, 8, 9, 7])
print(len(b))  # 4
print(b.shape)  # (4,)
print(len(np.array([], dtype=int)))  # 0
```

## Common mistakes

- **Float output.** `np.zeros` gives floats by default.
  - Pass `dtype=int` so the result is an integer array.
- **Using only one index array.** Indexing with `labels` alone selects whole rows, not single cells.
  - Use a row index array and a column index array together.
- **Mismatched index lengths.** Row and column indices must have the same length.
  - Build the row indices from the number of labels.
- **Swapping the shape order.** The shape is `(n, num_classes)`, not `(num_classes, n)`.
  - Check `.shape` on a small case.
- **Forgetting the empty case.** With `n = 0` the result must have shape `(0, num_classes)`.
  - Building from the shape and `np.arange` handles this without a special case.

## Hints

### Hint 1
- Make a table of zeros with one row per label and one column per class.
- For each row, switch on the one cell whose column is that row's label.
- Do all rows at once instead of looping.

### Hint 2
- `np.zeros` with an integer dtype gives the table, shape `(n, num_classes)`.
- `np.arange(n)` gives the row numbers, shape `(n,)`.
- Index the table with the row numbers and `labels` together, then assign `1`; the shape stays `(n, num_classes)`.

### Hint 3
- Fancy indexing with two arrays of length `n` selects cells `(rows[0], cols[0])`, `(rows[1], cols[1])`, and so on.
- Let the rows be `0, 1, ..., n-1` and let the columns be the labels themselves.
- Then cell `i` is exactly `(i, labels[i])`, where row `i` needs its `1`.
- Assign `1` to all those cells in one statement, then return the table.
