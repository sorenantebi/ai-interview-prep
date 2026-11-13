# Learn: Image to Patches

## The idea

- The task is to cut every image into small squares and flatten each square into one vector.
- Input shape is `(B, C, H, W)`. Output shape is `(B, N, C·patch·patch)`.
- It is only rearranging pixels: nothing is added, averaged or dropped.
- In ML this is the first step of a **Vision Transformer (ViT)**.
  - The model treats the patch vectors like the words of a sentence.
- **Patch**: a non-overlapping `patch × patch` square of the image, taken across all channels.
- **Patch grid**: the layout of the patches, `H/patch` rows by `W/patch` columns.
- **Row-major order**: left to right, then top to bottom, so the last index changes fastest.
- **View**: a tensor that shares memory with another one and just reads it in a different order.
- **Contiguous**: the values sit in memory in the order you'd read them row by row.
  - Reordering axes usually gives a non-contiguous view, and flattening that view forces a copy.

## Work it by hand

Example 1: one 4×4 image, one channel, `patch = 2`.

```text
 0  1  2  3
 4  5  6  7
 8  9 10 11
12 13 14 15
```

1. **Split each spatial axis in two.**
   - Height 4 becomes (2 grid rows, 2 offsets), and width 4 becomes (2 grid columns, 2 offsets).
   - Shape `(1, 1, 4, 4)` becomes `(1, 1, 2, 2, 2, 2)`.
   - The axes mean: batch, channel, grid row, row offset, grid column, column offset.
2. **Reorder the axes** so the grid comes first and the pixel offsets come last.
   - New meaning: batch, grid row, grid column, channel, row offset, column offset.
   - Shape `(1, 2, 2, 1, 2, 2)`.
3. **Read off each patch.** Fix a grid row and a grid column to get one 2×2 block:

| grid row | grid col | block | flattened |
|---|---|---|---|
| 0 | 0 | `[[0,1],[4,5]]` | `0,1,4,5` |
| 0 | 1 | `[[2,3],[6,7]]` | `2,3,6,7` |
| 1 | 0 | `[[8,9],[12,13]]` | `8,9,12,13` |
| 1 | 1 | `[[10,11],[14,15]]` | `10,11,14,15` |

4. **Merge axes.**
   - The two grid axes merge into `N = 2·2 = 4`.
   - The last three axes (channel, row offset, column offset) merge into `1·2·2 = 4`.
   - Final shape `(1, 4, 4)`:

```text
[[[0,1,4,5],[2,3,6,7],[8,9,12,13],[10,11,14,15]]]
```

## Tools you'll need

### tensor.reshape(*shape)

- Gives the same values a new shape. The total number of elements must stay the same.
- Values are read in row-major order, so the last axis changes fastest.
- One axis may be `-1`, and PyTorch works out its size.

```python
import torch

t = torch.arange(12)
print(t.reshape(3, 4).shape)      # torch.Size([3, 4])
print(t.reshape(2, 2, 3).shape)   # torch.Size([2, 2, 3])
print(t.reshape(2, -1).shape)     # torch.Size([2, 6])
```

### Splitting one axis into two

- `reshape` can split an axis of length `a·b` into `(a, b)`.
- The first new axis is "which block", and the second is "offset inside the block".

```python
import torch

s = torch.arange(6).reshape(3, 2)
print(s.tolist())  # [[0, 1], [2, 3], [4, 5]]
# row i is the block of original positions 2*i and 2*i+1
```

### tensor.permute(*dims)

- Reorders the axes: `x.permute(2, 0, 1)` makes old axis 2 the new axis 0, and so on.
- It returns a view, so no data moves yet, and the result is usually not contiguous.
- The values along each axis keep their order. Only the axes swap places.

```python
import torch

x = torch.zeros(2, 3, 4)
y = x.permute(2, 0, 1)
print(y.shape)            # torch.Size([4, 2, 3])
print(y.is_contiguous())  # False
```

### reshape after permute

- `reshape` copies when it has to, so it works on non-contiguous tensors.
- `view` refuses and raises an error instead.
- The copy follows the axis order as it is now, not the original memory order.

```python
import torch

m = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(m.permute(1, 0).reshape(-1).tolist())  # [1, 4, 2, 5, 3, 6]
print(m.reshape(-1).tolist())                # [1, 2, 3, 4, 5, 6]
try:
    m.permute(1, 0).view(-1)
except RuntimeError:
    print("view failed")                     # view failed
```

## Common mistakes

- **Flattening without permuting.**
  - After the split, the axes are `(B, C, gh, p, gw, p)`, so a plain flatten mixes pixels from different patches.
  - Write down what each axis means before you permute.
- **Putting channel after the offsets.**
  - The problem wants channel 0's whole `p×p` block, then channel 1's.
  - The last three axes must be `(C, p, p)`, not `(p, p, C)`.
- **Swapping grid row and grid column.**
  - Row-major means the grid column changes fastest, so the grid row comes first.
- **Using `view` after `permute`.**
  - It fails because the tensor isn't contiguous. Use `reshape`.
- **Using `/` for sizes.**
  - `H / p` is a float, and `reshape` rejects it. Use `//`.
- **Changing the dtype.**
  - Don't call `.float()`. Reshape and permute keep the dtype on their own.

## Hints

### Hint 1
- Split height and width each into "grid index" and "offset inside the patch".
- Reorder the axes so the grid axes come first, then channel, then the offsets.
- Merge the two grid axes into one axis.
- Merge channel and the two offsets into one axis.

### Hint 2
- Use `reshape` to get a 6-D tensor of shape `(B, C, H//p, p, W//p, p)`.
- Use `permute` to get shape `(B, H//p, W//p, C, p, p)`.
- Finish with `reshape` to `(B, N, C*p*p)`.
  - The two grid axes become `N`, and the last three become the patch vector.

### Hint 3
- After the split, the axes are numbered 0 to 5: batch, channel, grid row, row offset, grid column, column offset.
- You want them in this order: batch (0), grid row (2), grid column (4), channel (1), row offset (3), column offset (5).
  - That list of six numbers is the argument list for `permute`.
- The last reshape merges axes 1 and 2 into one axis of size `(H//p)·(W//p)`.
- It also merges axes 3, 4 and 5 into one axis of size `C·p·p`.
