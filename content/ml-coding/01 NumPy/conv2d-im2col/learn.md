# Learn: Conv2D with im2col

## The idea

- **Convolution** (2-D, "valid"): slide a small grid of numbers over an image and, at each position, produce one output number.
  - At each position, multiply the grid with the image patch under it, entry by entry, then add everything up.
  - That one number becomes one pixel of the output.
- **Kernel**: the small grid of weights (shape `(kh, kw)`).
- **Valid** means the kernel never hangs over the edge, so the output shape is `(H - kh + 1, W - kw + 1)`.
- **Cross-correlation**: deep-learning libraries do not flip the kernel, so you don't flip it either.
- Where it shows up: the forward pass of every conv layer in a CNN is this operation.
- **im2col** ("image to columns"): copy every patch into one row of a big matrix, then do a single matrix product.
  - Python loops over pixels are slow; matrix products are heavily optimised.
- **Fancy indexing**: indexing an array with other integer arrays; NumPy gathers one element per index combination.
- **Broadcasting**: NumPy stretches arrays of different shapes to a common shape, e.g. `(3, 1) + (1, 4)` gives `(3, 4)`.

## Work it by hand

Example 1: image is 3x3 with values 1..9, kernel is `[[1, 0], [0, -1]]`.

1. Output size: `oh = 3 - 2 + 1 = 2`, `ow = 2`, so 4 output pixels.
2. Output pixel `(i, j)` uses image rows `i, i+1` and columns `j, j+1`.
3. Flatten each patch into a row of 4 values. The im2col matrix has shape `(4, 4)`:

| output (i, j) | patch row |
|---|---|
| (0, 0) | 1 2 4 5 |
| (0, 1) | 2 3 5 6 |
| (1, 0) | 4 5 7 8 |
| (1, 1) | 5 6 8 9 |

4. Flatten the kernel: `[1, 0, 0, -1]`, shape `(4,)`.
5. Matrix product, one dot product per row:
   - `1*1 + 0*2 + 0*4 + (-1)*5 = -4`
   - `2 - 6 = -4`
   - `4 - 8 = -4`
   - `5 - 9 = -4`
6. The product has shape `(4,)`: `[-4, -4, -4, -4]`.
7. Reshape to `(2, 2)`: `[[-4, -4], [-4, -4]]`, which matches the expected output.

## Tools you'll need

### np.arange(n)
- Makes `[0, 1, ..., n-1]`.
- Use it to build index values.

```python
import numpy as np
a = np.arange(4)
print(a)  # [0 1 2 3]
print(a.shape)  # (4,)
```

### Adding an axis with `[:, None]`
- Indexing with `None` inserts a length-1 axis.
- This turns a 1-D array into a column or row so broadcasting can combine two arrays.

```python
import numpy as np
r = np.arange(3)[:, None] * 10 + np.arange(2)[None, :]
print(r)  # [[ 0  1]
          #  [10 11]
          #  [20 21]]
print(r.shape)  # (3, 2)
```

### Fancy indexing with index arrays
- `x[rows, cols]` broadcasts `rows` and `cols` together and returns one element per pair.
- The result has the broadcast shape of the indices, not the shape of `x`. 4-D index arrays give a 4-D result.

```python
import numpy as np
x = np.array([[10, 11, 12], [20, 21, 22]])
print(x[np.array([0, 1]), np.array([2, 0])])  # [12 20]
rr = np.array([[0], [1]])
cc = np.array([[0, 2]])
print(x[rr, cc])  # [[10 12]
                  #  [20 22]]
```

### .reshape(...)
- Changes the shape without changing the data order (row-major).
- `-1` means "work this size out for me"; the total element count must stay the same.

```python
import numpy as np
a = np.arange(12).reshape(2, 3, 2)
print(a.reshape(6, 2).shape)  # (6, 2)
print(a.reshape(-1).shape)  # (12,)
```

### The `@` operator
- Matrix product.
- A `(n, m)` matrix times an `(m,)` vector gives an `(n,)` vector: each row is dotted with the vector.

```python
import numpy as np
M = np.array([[1, 2, 3], [4, 5, 6]])
v = np.array([1, 0, -1])
print(M @ v)  # [-2 -2]
print((M @ v).shape)  # (2,)
```

## Common mistakes

- **Flipping the kernel.** True mathematical convolution flips it; here you don't. Use the formula exactly as given.
- **Wrong output size.** It is `H - kh + 1`, not `H - kh`. Check with Example 2: width 4, kernel width 3 gives 2 outputs.
- **Index arrays that don't broadcast.** Row indices `(oh, kh)` and column indices `(ow, kw)` won't line up as they are. Insert `None` axes so both become 4-D with the right axes aligned.
- **Wrong axis order before reshaping.** The patch array must be ordered `(oh, ow, kh, kw)`. Then reshaping to `(oh*ow, kh*kw)` gives one row per output pixel, with values in the same order as the flattened kernel.
- **Forgetting to reshape the result.** The matrix product returns a flat vector; turn it back into `(oh, ow)`.

## Hints

### Hint 1
- Work out the output size.
- For every output pixel, list which image rows and columns its patch covers.
- Collect all patches into a matrix with one row per output pixel.
- Flatten the kernel and multiply the matrix by it.
- Reshape the result to the output grid.

### Hint 2
- Build row indices from two `arange`s with broadcasting: shape `(oh, kh)`.
- Build column indices the same way: shape `(ow, kw)`.
- Add `None` axes so both broadcast to 4-D, then index the image: shape `(oh, ow, kh, kw)`.
- Reshape to `(oh*ow, kh*kw)`.
- Use `@` with the flattened kernel `(kh*kw,)`: shape `(oh*ow,)`.
- Reshape to `(oh, ow)`.

### Hint 3
- For output pixel `(i, j)` and kernel offset `(u, v)`, you want `image[i + u, j + v]`.
- The row index depends only on axes `i` and `u`; the column index only on axes `j` and `v`.
- Put the row array on axes 0 and 2 of a 4-D shape, with size 1 on axes 1 and 3.
- Put the column array on axes 1 and 3, with size 1 on axes 0 and 2.
- Indexing with both gives a result of shape `(oh, ow, kh, kw)`.
