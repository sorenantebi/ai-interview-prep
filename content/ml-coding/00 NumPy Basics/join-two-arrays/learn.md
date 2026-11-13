# Learn: Join Two Arrays

## The idea

- **The task:** glue two same-shaped tables of numbers, `a` and `b`, together in three different ways.
  - One on top of the other.
  - Side by side.
  - "Layered" like two sheets of paper in a pile.
- The function returns all three results as one tuple, in that order.
- **Axis:** one direction of an array.
  - Axis 0 runs down the rows.
  - Axis 1 runs across the columns.
- **Shape:** the tuple of axis lengths.
  - A `(2, 2)` array has 2 rows and 2 columns.
  - A `(2, 2, 2)` array is like two `(2, 2)` tables in one block.
- The first two joins **grow an axis that already exists**.
- The third join **creates a brand-new axis** of length 2, so each position `(i, j)` holds a pair: one value from `a`, one from `b`.
- **Where it shows up in ML and data work:**
  - Appending a new batch of samples to a dataset (vertical).
  - Attaching extra feature columns to a feature matrix (horizontal).
  - Pairing predictions with labels so each sample carries both (new axis).

## Work it by hand

Example 1: `a = [[1, 2], [3, 4]]`, `b = [[5, 6], [7, 8]]`. Both have shape `(2, 2)`.

1. **Vertical:** write the rows of `a`, then the rows of `b` underneath.
   - Result: `[[1,2],[3,4],[5,6],[7,8]]`
   - Shape: `(4, 2)`, that is `(2m, n)`.
2. **Horizontal:** extend each row of `a` with the same row of `b`.
   - Row 0: `[1,2]` + `[5,6]` = `[1,2,5,6]`
   - Row 1: `[3,4]` + `[7,8]` = `[3,4,7,8]`
   - Result: `[[1,2,5,6],[3,4,7,8]]`
   - Shape: `(2, 4)`, that is `(m, 2n)`.
3. **Stacked:** go cell by cell, pairing `a[i, j]` with `b[i, j]`.
   - `(0, 0)`: `[1, 5]`
   - `(0, 1)`: `[2, 6]`
   - `(1, 0)`: `[3, 7]`
   - `(1, 1)`: `[4, 8]`
   - Group them by row: `[[[1,5],[2,6]],[[3,7],[4,8]]]`
   - Shape: `(2, 2, 2)`, that is `(m, n, 2)`.
4. **Return** the three arrays as a tuple. Printed with 5 decimals, this is exactly the expected output of Example 1.

## Tools you'll need

### np.concatenate((x, y), axis=0)

- Joins arrays along an **existing** axis; all other axes must match in length.
- `axis=0` puts rows below; `axis=1` adds columns to the right.
- The arrays go in as **one tuple** (or list), not as separate arguments.

```python
import numpy as np

x = np.array([[1, 2, 3]])
y = np.array([[4, 5, 6]])
print(np.concatenate((x, y), axis=0).shape)  # (2, 3)
print(np.concatenate((x, y), axis=1).shape)  # (1, 6)
```

### np.vstack((x, y))

- "Vertical stack": puts `y`'s rows below `x`'s rows.
- For 2-D arrays it equals `concatenate` with `axis=0`.
- The column counts must match.

```python
import numpy as np

x = np.zeros((2, 3))
y = np.ones((4, 3))
print(np.vstack((x, y)).shape)  # (6, 3)
```

### np.hstack((x, y))

- "Horizontal stack": puts `y`'s columns to the right of `x`'s.
- For 2-D arrays it equals `concatenate` with `axis=1`.
- The row counts must match.

```python
import numpy as np

x = np.zeros((2, 3))
y = np.ones((2, 1))
print(np.hstack((x, y)).shape)  # (2, 4)
```

### np.stack((x, y), axis=k)

- Joins arrays of **identical shape** along a **new** axis inserted at position `k`.
- The result has one more dimension than the inputs.
- Negative `axis` counts from the end of the result, so `-1` is the last axis.

```python
import numpy as np

x = np.array([10, 20, 30])
y = np.array([1, 2, 3])
print(np.stack((x, y), axis=0).shape)  # (2, 3)
print(np.stack((x, y), axis=1).shape)  # (3, 2)
print(np.stack((x, y), axis=1)[0])     # [10  1]
```

### .shape

- A tuple of axis lengths; print it whenever you are unsure.
- It tells you whether an axis grew or a new one appeared.

```python
import numpy as np

x = np.zeros((3, 5))
print(x.shape)     # (3, 5)
print(x.shape[0])  # 3
```

## Common mistakes

- **Passing two arguments instead of one tuple.** `np.vstack(a, b)` fails.
  - Use double parentheses: `np.vstack((a, b))`.
- **Mixing up axis 0 and axis 1.** Axis 0 is rows (on top), axis 1 is columns (side by side).
  - Check your output shapes against `(2m, n)` and `(m, 2n)`.
- **Using `concatenate` when you need a new axis.** It never adds a dimension, so the result stays 2-D.
  - Only `stack` gives the `(m, n, 2)` shape.
- **Putting the new axis in the wrong place.** `axis=0` gives `(2, m, n)`, not `(m, n, 2)`.
  - Pick the axis so the length-2 dimension ends up last.
- **Returning in the wrong order.** The tuple must be vertical, horizontal, stacked.

## Hints

### Hint 1
- You need three independent joins.
- The first extends the row axis (`a` on top of `b`).
- The second extends the column axis (`a` next to `b`).
- The third makes a new axis of length 2 at the end.
- Compute each one separately, then return them together as a tuple.

### Hint 2
- Step 1: a row-wise joining tool gives shape `(2m, n)`.
- Step 2: a column-wise joining tool gives shape `(m, 2n)`.
- Step 3: `np.stack` with the right `axis` gives shape `(m, n, 2)`.
- Remember that the inputs go in as one tuple, like `(a, b)`.

### Hint 3
- For the third result, the new axis must come after both existing axes.
  - The inputs have axes 0 and 1, so the new one is axis 2 (or -1).
- Then `result[i, j]` is a length-2 vector holding `a[i, j]` first and `b[i, j]` second.
- Finally, return the three arrays in the order vertical, horizontal, stacked.
