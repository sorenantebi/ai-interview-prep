# Learn: Pad Sequences

## The idea

- The task: turn a ragged list of lists into one rectangular tensor, plus a record of the true lengths.
- **Padding** means adding a filler value (`pad_value`) to the end of short sequences until every row is as long as the longest.
- Models need rectangular input because a batch is one big tensor. Rows of different lengths can't be stacked.
- This pair (padded batch plus lengths) shows up in almost every NLP training loop, just before an embedding layer or an attention mask.
- **Tensor**: PyTorch's n-dimensional array.
- **dtype**: the element type of a tensor. Here both outputs must be `torch.int64`, also written `torch.long`.
- **Shape**: the size along each dimension. `(N, L)` means `N` rows and `L` columns.
- **Boolean mask**: a `True`/`False` tensor that marks which positions of another tensor to read or overwrite.
- **Broadcasting**: when two tensors of different shapes are combined, size-1 dimensions are stretched to match.
  - `(N, 1)` against `(L,)` gives `(N, L)`.
- **Row-major order**: reading a 2-D tensor row by row, left to right. Mask assignment uses this order.

## Work it by hand

Example 1: `seqs = [[1, 2, 3], [4]]`, `pad_value = 0`.

| Step | Result | Shape |
|---|---|---|
| 1. Length of each sequence | `[3, 1]` | `(2,)` |
| 2. Longest length `L` | `3` | scalar |
| 3. Grid filled with `pad_value` | `[[0,0,0],[0,0,0]]` | `(2, 3)` |
| 4. Column positions | `[0, 1, 2]` | `(3,)` |
| 5. Lengths as a column | `[[3],[1]]` | `(2, 1)` |
| 6. Is position < length? | `[[T,T,T],[T,F,F]]` | `(2, 3)` |
| 7. All tokens, in order, as one flat list | `[1, 2, 3, 4]` | `(4,)` |
| 8. Write tokens into the `True` slots | `[[1,2,3],[4,0,0]]` | `(2, 3)` |

- The mask has four `True` slots and there are four tokens.
- Row 0's three slots get `1, 2, 3`, then row 1's one slot gets `4`.
- Final output: `[[[1,2,3],[4,0,0]], [3,1]]`.

## Tools you'll need

### torch.tensor(data, dtype=...)
- Builds a tensor from a Python list.
- Pass `dtype=torch.long` to force int64. This matters for empty lists, which default to float.

```python
import torch

t = torch.tensor([5, 6, 7], dtype=torch.long)
print(t.dtype)  # torch.int64
print(t.shape)  # torch.Size([3])
print(torch.tensor([]).dtype)  # torch.float32
```

### torch.full(size, fill_value, dtype=...)
- Makes a tensor of the given shape (a tuple) with every entry equal to `fill_value`.
- A zero in the size is allowed and gives an empty tensor.

```python
import torch

a = torch.full((2, 4), 9, dtype=torch.long)
print(a.tolist())  # [[9, 9, 9, 9], [9, 9, 9, 9]]
print(torch.full((3, 0), 9, dtype=torch.long).shape)  # torch.Size([3, 0])
```

### torch.arange(n)
- Returns `[0, 1, ..., n-1]` as an int64 tensor, handy as a "column index" vector.
- `arange(0)` is a valid empty tensor.

```python
import torch

print(torch.arange(4).tolist())  # [0, 1, 2, 3]
print(torch.arange(0).shape)  # torch.Size([0])
```

### Tensor.max() and int(...)
- `.max()` returns a 0-dim tensor, not a plain number.
- Wrap it in `int(...)` when you need a Python int, for example inside a shape tuple.

```python
import torch

x = torch.tensor([2, 8, 5])
print(x.max())  # tensor(8)
print(int(x.max()))  # 8
```

### x[:, None] / unsqueeze(1), and broadcasting
- `x[:, None]` and `x.unsqueeze(1)` both turn shape `(N,)` into `(N, 1)`.
- Comparing `(N, 1)` with `(L,)` broadcasts to an `(N, L)` boolean tensor.

```python
import torch

cols = torch.arange(4)         # shape (4,)
lim = torch.tensor([2, 0, 3])  # shape (3,)
m = cols < lim[:, None]        # (4,) vs (3, 1) -> (3, 4)
print(m.shape)  # torch.Size([3, 4])
print(m.tolist())  # [[True, True, False, False], [False, False, False, False], [True, True, True, False]]
```

### Boolean mask assignment: t[mask] = values
- Wherever `mask` is `True`, the slot is overwritten by the next value from the 1-D `values`, in row-major order.
- The number of values must equal the number of `True` entries.

```python
import torch

t = torch.zeros(2, 3, dtype=torch.long)
mask = torch.tensor([[True, False, True], [False, True, False]])
t[mask] = torch.tensor([10, 20, 30])
print(t.tolist())  # [[10, 0, 20], [0, 30, 0]]
```

### Flattening a list of lists
- A nested list comprehension joins many lists into one flat list, keeping order.
- Empty inner lists simply contribute nothing.

```python
nested = [[9], [8, 7], []]
flat = [v for row in nested for v in row]
print(flat)  # [9, 8, 7]
```

## Common mistakes

- **Wrong dtype.** `torch.tensor([])` is float, and a float fill gives a float grid. Always pass `dtype=torch.long`.
- **Forgetting the extra dimension.** Comparing `(L,)` with `(N,)` fails or gives nonsense. Make the lengths `(N, 1)` so the result is `(N, L)`.
- **Flattening in the wrong order.** Mask assignment fills row by row, so tokens must be sequence 0, then sequence 1, and so on. Don't sort or transpose.
- **Empty sequences.** They have length 0 and add nothing to the flat list. If all are empty, `L = 0` and the flat token tensor is empty, so its dtype must still be `long`.
- **A Python loop per row.** Assigning `padded[i, :n] = ...` per row works but is what the problem asks you to avoid.

## Hints

### Hint 1
- Get the length of every sequence, and the maximum length.
- Create a grid of the right size filled with the padding value.
- Work out which grid cells should hold real tokens.
- Put all the tokens into those cells in one operation.
- Return the padded grid and the lengths.

### Hint 2
- Lengths: `torch.tensor` over a list of `len(s)`, shape `(N,)`.
- Grid: `torch.full` with shape `(N, L)`, where `L` comes from `int(...max())`.
- Mask: `torch.arange(L)` compared with the lengths made into `(N, 1)`, giving a boolean `(N, L)`.
- Tokens: a nested list comprehension, converted with `torch.tensor(..., dtype=torch.long)`, shape `(total_tokens,)`.
- Assign the tokens through the mask.

### Hint 3
- Cell `(i, j)` holds a real token exactly when `j < lengths[i]`.
- Column indices `[0..L-1]` form a row vector, and the lengths form a column `(N, 1)`. Broadcasting compares every pair and produces the `(N, L)` mask.
- The number of `True` cells equals the sum of the lengths, which equals the number of flat tokens.
- Both the mask and the flat list are ordered row by row, so row 0's tokens land first, then row 1's, and so on.
- The all-empty case needs no special handling if the flat tensor has `dtype=torch.long`.
