# Learn: Masked Mean

## The idea

- **The task:** for each sequence in a batch, average its real token vectors and ignore the padding.
- **Padding:** sequences have different lengths, so short ones are filled up to a common length `T` with junk values.
- **Mask:** a tensor of 1s and 0s saying which positions are real (1) and which are padding (0).
- **Where it shows up:**
  - Pooling token embeddings into one sentence embedding in NLP.
  - Averaging a loss over real tokens only, in a training loop.
- **Broadcasting:** PyTorch stretches a size-1 axis to match the other tensor's size during element-wise maths.
  - Shapes are compared from the right.
- **dtype:** a tensor's number type, such as `torch.int64` or `torch.float32`.
  - The mask is integer but `x` is float, so you need to match them.
- **Empty sequence:** a count of 0 means dividing `0 / 0`, which gives `nan`.
  - The answer must be 0 instead, so you need a way around that.
- **Big idea:** make the padding contribute nothing to a sum, then divide by how many real tokens there were.

## Work it by hand

Example 1: `x` has shape `(1, 3, 2)` and `mask = [[1, 1, 0]]` has shape `(1, 3)`.

| Step | Value | Shape |
|---|---|---|
| Start: `x` | `[[[1, 2], [3, 4], [100, 100]]]` | `(1, 3, 2)` |
| Mask as float, with a trailing axis | `[[[1], [1], [0]]]` | `(1, 3, 1)` |
| Multiply (padding becomes 0) | `[[[1, 2], [3, 4], [0, 0]]]` | `(1, 3, 2)` |
| Sum over the time axis | `[[4, 6]]` | `(1, 2)` |
| Count real tokens (sum of the mask over time) | `[[2]]` | `(1, 1)` |
| Divide: 4/2 and 6/2 | `[[2, 3]]` | `(1, 2)` |

- Final answer: `[[2.0, 3.0]]`, which matches the expected output.

The empty case from Example 2, first sequence with mask `[0, 0]`:

- The total is 0 and the count is 0, so `0 / 0` would be `nan`.
- If the count is forced to be at least 1, you get `0 / 1 = 0`, the required answer.
- A count that was already 2 or more stays unchanged.

## Tools you'll need

### `tensor.to(dtype)`
- Returns a copy of the tensor with another dtype.
- Cast the mask to `x.dtype` so arithmetic and division stay float.

```python
import torch
a = torch.tensor([3, 0, 7])
print(a.dtype)  # torch.int64
b = a.to(torch.float32)
print(b.dtype)  # torch.float32
print(b / 2)  # tensor([1.5000, 0.0000, 3.5000])
```

### `tensor.unsqueeze(dim)`
- Inserts a new axis of size 1 at position `dim`.
- `-1` means "at the end".
- This lets a `(B, T)` tensor line up with a `(B, T, D)` tensor.

```python
import torch
m = torch.tensor([[1, 0, 1, 1], [0, 0, 1, 0]])
print(m.shape)  # torch.Size([2, 4])
print(m.unsqueeze(-1).shape)  # torch.Size([2, 4, 1])
print(m.unsqueeze(0).shape)  # torch.Size([1, 2, 4])
```

### Broadcasting with `*`
- Shapes are compared from the right.
- An axis of size 1 is stretched to match the other tensor.
- Axes must match or be 1; otherwise PyTorch raises an error.

```python
import torch
a = torch.ones(2, 3, 4)
w = torch.tensor([1., 2., 3.]).reshape(1, 3, 1)
print((a * w).shape)  # torch.Size([2, 3, 4])
print((a * w)[0, :, 0])  # tensor([1., 2., 3.])
```

### `tensor.sum(dim=...)`
- Adds up values along one axis, and that axis disappears from the shape.
- `keepdim=True` keeps it as size 1 instead.

```python
import torch
t = torch.arange(24.).reshape(2, 3, 4)
print(t.sum(dim=1).shape)  # torch.Size([2, 4])
print(t.sum(dim=1, keepdim=True).shape)  # torch.Size([2, 1, 4])
print(t.sum(dim=2)[0])  # tensor([ 6., 22., 38.])
```

### `tensor.clamp(min=...)`
- Raises every value below `min` up to `min`.
- Values already above it are unchanged.

```python
import torch
c = torch.tensor([0., 2., 5.])
print(c.clamp(min=1))  # tensor([1., 2., 5.])
```

## Common mistakes

- **Integer mask with float `x`, or integer division.**
  - Cast the mask to `x`'s dtype before multiplying and dividing, so the mean stays a float.
- **Summing over the wrong axis.**
  - Time is `dim=1` in `(B, T, D)`.
  - Summing `dim=2` gives one number per token, not per sequence.
- **Forgetting the extra axis on the mask.**
  - A `(B, T)` mask lines up with the last two axes `(T, D)` of `x`, so it errors or gives wrong results.
  - Add a trailing axis first.
- **Dividing by zero for empty sequences.**
  - `0 / 0` is `nan`.
  - Make sure the count is at least 1 before dividing.
- **Letting padding leak in.**
  - Padding values can be huge, so don't average everything and fix it afterwards.
  - Zero the padding first, then sum.

## Hints

### Hint 1
- Turn the padding into zeros so it cannot add anything to a sum.
- Add up the tokens of each sequence.
- Count how many real tokens each sequence has.
- Divide the totals by the counts.
- Make sure a count of zero cannot cause a bad division.

### Hint 2
- Convert the mask to `x`'s dtype with `.to(...)`, then `unsqueeze(-1)`. The mask now has shape `(B, T, 1)`.
- Multiply with `x`. Broadcasting gives `(B, T, D)`, with padding zeroed.
- `sum(dim=1)` gives totals of shape `(B, D)`.
- Summing the mask over `dim=1` gives counts of shape `(B, 1)`.
- `clamp(min=1)` on the counts fixes the zero cases, and the division broadcasts to `(B, D)`.

### Hint 3
- For sequence `b`, the total is the sum over `t` of `x[b, t] * mask[b, t]`, a vector of size `D`.
- The count is the sum over `t` of `mask[b, t]`, a single number per sequence.
- The result is `total / max(count, 1)`.
- The `(B, 1)` count divides the `(B, D)` totals by broadcasting, one count per row.
- Take the mask's dtype from `x`, so the division is a float division.
