# Learn: Reverse, Stride and Crop

## The idea

- The task is to cut two new arrays out of one 2-D grid using only **slicing**.
  - **Slicing** means picking part of an array with the `start:stop:step` syntax.
- `flipped` is the grid turned upside down, keeping only every other column.
- `block` is a rectangle cut from the **original** grid.
- Slicing shows up all over ML and data work:
  - cutting a batch out of a dataset
  - cropping a region of an image
  - flipping an image for data augmentation
  - taking every k-th sample to thin out a time series
- A **row** is one horizontal line of the grid (axis 0).
- A **column** is one vertical line (axis 1).
- A **view** is a new array object that looks at the same memory as the original, with no copy of the numbers.
  - Basic slices give views, so they are fast.

## Work it by hand

Example 1: `a` has shape `(3, 4)`, with `r0 = 1, r1 = 3, c0 = 1, c1 = 3`.

```text
[[ 1,  2,  3,  4],
 [ 5,  6,  7,  8],
 [ 9, 10, 11, 12]]
```

**Part 1: `flipped`**

| Step | Action | Result | Shape |
|---|---|---|---|
| 1 | Reverse the row order | `[9,10,11,12]`, `[5,6,7,8]`, `[1,2,3,4]` | (3, 4) |
| 2 | Keep columns 0 and 2 (skip 1 and 3) | `[9,11]`, `[5,7]`, `[1,3]` | (3, 2) |

**Part 2: `block`** (start again from the original `a`, not from `flipped`)

| Step | Action | Result | Shape |
|---|---|---|---|
| 1 | Keep rows 1 up to, not including, 3 (rows 1 and 2) | `[5,6,7,8]`, `[9,10,11,12]` | (2, 4) |
| 2 | Keep columns 1 up to, not including, 3 (columns 1 and 2) | `[6,7]`, `[10,11]` | (2, 2) |

Final answer, printed as floats: `([[9,11],[5,7],[1,3]], [[6,7],[10,11]])`

## Tools you'll need

### Basic slicing `x[start:stop:step]`

- `start` is included, `stop` is excluded, and `step` is how far to jump.
- Any part can be left out. The defaults are the beginning, the end and a step of 1.

```python
import numpy as np

x = np.array([20, 21, 22, 23, 24, 25, 26])
print(x[2:5])   # [22 23 24]
print(x[:3])    # [20 21 22]
print(x[::3])   # [20 23 26]
```

### Negative step

- A negative step walks backwards.
- With no start or stop, a step of `-1` gives the whole array reversed.

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5, 6])
print(x[::-1])    # [6 5 4 3 2 1]
print(x[::-2])    # [6 4 2]
```

### Slicing in 2-D: one slice per axis

- Separate the slices with a comma. The first slice applies to rows (axis 0), the second to columns (axis 1).
- The result is still 2-D, so check `.shape` when unsure.

```python
import numpy as np

g = np.arange(12).reshape(3, 4)
print(g[1:3, 0:2])    # [[4 5]
                      #  [8 9]]
print(g[1:3, 0:2].shape)  # (2, 2)
print(g[:, ::-1][0])  # [3 2 1 0]
print(g[::2].shape)   # (2, 4)
```

### Views versus copies

- A basic slice shares memory with the original, so changing the slice changes the original.
- Call `.copy()` if you need an independent array.

```python
import numpy as np

g = np.zeros((2, 3))
v = g[:, :2]
v[0, 0] = 9
print(g[0, 0])   # 9.0
```

## Common mistakes

- **Treating `stop` as included.**
  - `r0:r1` stops before `r1`, so rows 1 to 3 means rows 1 and 2.
  - Pass the numbers straight through, without adding or subtracting 1.
- **Mixing up the axes.**
  - The first slot is rows and the second is columns.
  - Reversing the wrong axis gives a left-right mirror instead of an upside-down flip.
- **Cropping the flipped array.**
  - The block comes from the original `a`.
  - Cropping the flipped result gives different rows.
- **Expecting a step of 2 to keep 2 columns.**
  - A step of 2 keeps columns 0, 2, 4, and so on.
  - With `m` columns you keep `ceil(m / 2)` of them, so 5 columns give 3.
- **Reaching for a loop.**
  - Slicing already does the work in one expression per array.

## Hints

### Hint 1
- Build two separate arrays, both taken straight from the original `a`.
- For the first, reverse the rows and thin out the columns.
- For the second, cut out the rectangle.
- Return both together as a tuple.

### Hint 2
- Both arrays use 2-D slicing: one slice for rows, then one for columns.
- The first result has `n` rows and `ceil(m / 2)` columns.
- The second result has shape `(r1 - r0, c1 - c0)`.
- Return the pair in the order flipped, then block.

### Hint 3
- First array:
  - The row slice has no start, no stop and a step of -1.
  - The column slice has no start, no stop and a step of 2.
- Second array:
  - The row slice runs from `r0` to `r1`.
  - The column slice runs from `c0` to `c1`.
  - Neither slice needs a step.
- Put the two results in a tuple as `(flipped, block)`.
