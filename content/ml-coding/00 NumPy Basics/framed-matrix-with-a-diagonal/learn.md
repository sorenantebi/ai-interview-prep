# Learn: Framed Matrix with a Diagonal

## The idea

- The task is to build an `n x n` grid of numbers in three layers: border, inside, diagonal.
  - The **border** is the first and last row and the first and last column. It is all `1`.
  - The **inside** is everything else. It is all `0`.
  - The **main diagonal** runs from top-left to bottom-right. It holds `value` and wins over the border at the corners.
- The goal is to build the whole array with a few array operations, not a loop over cells.
- This shows up in ML and data work all the time: masks, identity matrices, initial weights and padding.
- **Shape** is the size of each dimension. `(3, 3)` means 3 rows and 3 columns.
- **Slice** is a range of positions, like `a[1:-1]`, which skips the first and last.
- **Boolean mask** is an array of `True`/`False` with the same shape as another array.
  - It marks which cells to select or change.
- **Painting in layers** means later assignments cover earlier ones.
  - The order of your steps decides who wins where layers overlap.

## Work it by hand

Example 1: `n = 3`, `value = 5.0`. Paint layers, with later ones covering earlier ones.

1. **Start with every cell at one value.** Shape `(3, 3)`:

```text
1 1 1
1 1 1
1 1 1
```

2. **Clear the inside.** That is everything except the first and last row and column. For `n = 3` it is only the centre (row 1, column 1):

```text
1 1 1
1 0 1
1 1 1
```

3. **Mark the diagonal.** The cells are (0,0), (1,1), (2,2). As a mask, shape `(3, 3)`:

```text
T F F
F T F
F F T
```

4. **Paint `value` where the mask is True.** This covers the corners and the centre:

```text
5 1 1
1 5 1
1 1 5
```

- This matches the expected output `[[5,1,1],[1,5,1],[1,1,5]]`.
- The centre was `0`, but the diagonal covered it. The diagonal goes last so it wins.

## Tools you'll need

### np.ones(shape) and np.zeros(shape)

- Create an array filled with `1.0` or `0.0`.
- Pass the shape as a tuple. The default dtype is float.

```python
import numpy as np

a = np.zeros((2, 4))
b = np.ones((3, 2))
print(a.shape)  # (2, 4)
print(b)
# [[1. 1.]
#  [1. 1.]
#  [1. 1.]]
```

### np.full(shape, fill_value)

- Like `ones`, but with any number you choose.

```python
import numpy as np

c = np.full((2, 3), 9.5)
print(c)
# [[9.5 9.5 9.5]
#  [9.5 9.5 9.5]]
```

### np.eye(n, dtype=...)

- Makes an `n x n` array with `1` on the main diagonal and `0` elsewhere.
- With `dtype=bool` you get `True` on the diagonal and `False` elsewhere, a ready-made mask.

```python
import numpy as np

print(np.eye(3))
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]
print(np.eye(2, dtype=bool))
# [[ True False]
#  [False  True]]
```

### Slice assignment: `a[r0:r1, c0:c1] = x`

- A slice selects a block. Assigning to it changes those cells in place.
- Negative indices count from the end, so `1:-1` means "skip the first and the last".
- An empty range (for example on a 2x2 array) changes nothing and raises no error.

```python
import numpy as np

a = np.ones((4, 5))
a[1:-1, 2:] = 7
print(a)
# [[1. 1. 1. 1. 1.]
#  [1. 1. 7. 7. 7.]
#  [1. 1. 7. 7. 7.]
#  [1. 1. 1. 1. 1.]]
```

### Boolean mask assignment: `a[mask] = x`

- If `mask` is a boolean array with the same shape as `a`, `a[mask] = x` sets every cell where the mask is `True`.

```python
import numpy as np

a = np.zeros((2, 3))
mask = np.array([[True, False, False],
                 [False, False, True]])
a[mask] = 4.0
print(a)
# [[4. 0. 0.]
#  [0. 0. 4.]]
```

## Common mistakes

- **Painting in the wrong order.** Setting the diagonal first and the rest afterwards erases it.
  - Do the diagonal last.
- **Forgetting small `n`.** For `n = 1` and `n = 2` there is no inside.
  - Check these by hand. For `n = 1` the one cell must end up as `value`.
- **Passing `n` instead of a tuple.** `np.ones(n)` gives a 1-D array.
  - Use `np.ones((n, n))` with double parentheses.
- **Using `np.eye(n)` as a mask without `dtype=bool`.** A float array of `0.0`/`1.0` inside `[...]` is read as index numbers, not a mask.
  - Add `dtype=bool`.
- **Writing `a[1:-1][1:-1]`.** That slices the rows twice.
  - Use one comma: `a[1:-1, 1:-1]`.

## Hints

### Hint 1
- Start with a grid where every cell is `1`.
- Set the inside to `0`.
- Put `value` on the diagonal last, so it overrides everything else.

### Hint 2
- Make the base with `np.ones` and a shape tuple, giving shape `(n, n)`.
- Set the inside with one slice assignment on rows and columns from 1 up to but not including the last. The shape stays `(n, n)`.
- Get a diagonal mask from `np.eye` with a boolean dtype, shape `(n, n)`.
- Assign `value` through that mask.

### Hint 3
- The inside is every cell whose row index and column index are both between 1 and `n-2`.
  - In slice form that is "from 1 to minus 1" on both axes, separated by a comma.
- The diagonal mask is `True` exactly where row equals column.
- Put that mask inside the square brackets on the left side of `=`, and `value` on the right.
