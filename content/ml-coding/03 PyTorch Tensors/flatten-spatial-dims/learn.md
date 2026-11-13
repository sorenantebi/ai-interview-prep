# Learn: Flatten Spatial Dims

## The idea

- The task: turn a grid of feature vectors into a sequence of feature vectors.
  - Input `(B, C, H, W)`: `B` images, each with `C` channel values at every cell of an `H` by `W` grid.
  - Output `(B, H*W, C)`: for each image, `H*W` tokens, each a vector of `C` numbers.
- This shows up when a transformer sits on top of a CNN backbone, as in vision transformers and detection models.
  - CNNs work on grids, but transformers read sequences of tokens.
- Two things must happen:
  - The two spatial axes `H` and `W` merge into one axis.
  - The channel axis moves from the middle to the end.
- **Token** here means one grid cell, written as its `C` channel values.
- **Row-major** means reading the grid row by row, like text on a page.
  - Token `t = h*W + w` is the cell at row `h`, column `w`.
- **Axis (dim)** is one direction of a tensor, counted from 0. In `(B, C, H, W)`, axis 0 is `B` and axis 3 is `W`.
- **View** is a tensor that shares memory with another and only changes how that memory is read.
  - Merging adjacent axes and swapping two axes can both be views, so nothing is copied.

## Work it by hand

Example 1: `x` has shape `(1, 2, 2, 2)`. Channel 0 is `[[1,2],[3,4]]` and channel 1 is `[[5,6],[7,8]]`.

| Step | What happens | Result | Shape |
|---|---|---|---|
| Start | one image, two 2x2 channels | ch0 `[[1,2],[3,4]]`, ch1 `[[5,6],[7,8]]` | `(1, 2, 2, 2)` |
| 1. Merge H and W | read each channel's grid row by row | ch0 `[1,2,3,4]`, ch1 `[5,6,7,8]` | `(1, 2, 4)` |
| 2. Move C last | swap the channel axis and the position axis | rows are positions, columns are channels | `(1, 4, 2)` |

- After step 2, position 0 holds (ch0, ch1) = `[1,5]`.
- Position 1 holds `[2,6]`, position 2 holds `[3,7]`, and position 3 holds `[4,8]`.
- Final answer: `[[[1,5],[2,6],[3,7],[4,8]]]`, which matches the expected output.

## Tools you'll need

### `t.flatten(start_dim)`

- Merges all axes from `start_dim` to the last one into a single axis, in row-major order.
- Axes before `start_dim` are left alone.

```python
import torch

a = torch.arange(12).reshape(2, 3, 2)
print(a.shape)  # torch.Size([2, 3, 2])
print(a.flatten(1).shape)  # torch.Size([2, 6])
print(a.flatten(1)[0].tolist())  # [0, 1, 2, 3, 4, 5]
```

### `t.reshape(...)` and `-1`

- Gives the same data a new shape. The total number of elements must stay the same.
- One size may be `-1`, meaning "work it out".
- It regroups data in memory order and does not move axes.

```python
import torch

m = torch.arange(6)
print(m.reshape(2, 3).tolist())  # [[0, 1, 2], [3, 4, 5]]
print(m.reshape(3, -1).shape)  # torch.Size([3, 2])
```

### `t.transpose(d0, d1)`

- Swaps exactly two axes and leaves the others in place.
- The result is a view.

```python
import torch

m = torch.arange(6).reshape(2, 3)
print(m.transpose(0, 1).tolist())  # [[0, 3], [1, 4], [2, 5]]
print(m.transpose(0, 1).shape)  # torch.Size([3, 2])
```

### `t.permute(*dims)`

- Reorders all axes at once.
- `permute(2, 0, 1)` puts old axis 2 first, then old axis 0, then old axis 1.
- It is handy when more than two axes must move.

```python
import torch

p = torch.zeros(2, 3, 4)
print(p.permute(2, 0, 1).shape)  # torch.Size([4, 2, 3])
```

### `t.is_contiguous()` and `t.contiguous()`

- After a transpose or permute, the memory order no longer matches the new shape, so the tensor is not **contiguous**.
- `.view` fails on such tensors; `.reshape` still works.
- `.contiguous()` makes a real copy in the new order.

```python
import torch

t = torch.arange(6).reshape(2, 3).transpose(0, 1)
print(t.is_contiguous())  # False
print(t.contiguous().is_contiguous())  # True
```

## Common mistakes

- **Reshaping straight to `(B, H*W, C)`.**
  - `reshape` only regroups memory order, so values land in the wrong tokens.
  - Merge `H` and `W` first, then move the channel axis.
- **Merging the wrong axes.**
  - Axes are counted from 0, and `B` and `C` must stay separate.
  - Pick the start axis that leaves them alone.
- **Swapping the wrong pair.**
  - After merging, the shape is `(B, C, H*W)`, so swapping axes 0 and 1 mixes up the batch.
  - Print `.shape` after each step.
- **Calling `.view` on the result.**
  - A transposed tensor is not contiguous, so `.view` raises an error.
  - Use `.reshape`, or call `.contiguous()` first if you need a real copy.
- **Changing the dtype or using loops.**
  - Tensor methods keep the dtype for you.
  - Rebuilding the result with `torch.tensor(...)` from a Python list can change it.

## Hints

### Hint 1
- Merge the two spatial axes into one, so each channel becomes one long row of positions.
- Move the channel axis from the middle to the end, so each position gets its own row of channel values.

### Hint 2
- Merge the last two axes with `flatten`; the shape becomes `(B, C, H*W)`.
- Swap the two non-batch axes with `transpose`; the shape becomes `(B, H*W, C)`.
- Check the shape after each step.

### Hint 3
- For `flatten`, count axes from 0: `B` is 0 and `C` is 1, so start at axis 2 to merge only `H` and `W`.
- For `transpose`, swap axis 1 (`C`) with axis 2 (`H*W`).
- Position `h*W + w` comes out right because `flatten` reads each channel's grid row by row.
