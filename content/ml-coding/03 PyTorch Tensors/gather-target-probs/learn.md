# Learn: Gather Target Probabilities

## The idea

- **The task:** for every example, pull out the one probability the model gave to the correct class.
- Each row of `probs` is a list of class probabilities, and the matching entry of `targets` says which column is the right one.
- The result has one number per example, so its shape is the shape of `targets`.
- **Where it shows up:** it is the core step of negative log-likelihood (NLL) loss.
  - NLL takes the probability of the true class, then applies `-log` to it.
  - Every classification training loop does this.
  - Language models do it at every token position, over the whole vocabulary.
- **Leading dimensions:** all dimensions except the last.
  - They say *which example* (or which sequence and token).
  - The last dimension is the class.
- **Target:** an integer class index, such as `1` for "the second class".
- **Gather:** picking elements from a tensor by index, instead of by slicing.
- **Index tensor:** a tensor of integer positions that tells `gather` what to pick.
  - It must have the same number of dimensions as the tensor you pick from.

## Work it by hand

Example 1: `probs` has shape `(2, 3)`, `targets = [1, 0]` has shape `(2,)`.

```text
probs = [[0.1, 0.7,  0.2 ],    row 0
         [0.5, 0.25, 0.25]]    row 1
targets = [1, 0]
```

1. Row 0 has target `1`. Look at `[0.1, 0.7, 0.2]` and take index 1, which is `0.7`.
2. Row 1 has target `0`. Look at `[0.5, 0.25, 0.25]` and take index 0, which is `0.5`.
3. Collect the picks: `[0.7, 0.5]`, shape `(2,)`. This matches the expected output `[0.70000, 0.50000]`.

| Row | Target | Row of probs      | Pick | Value |
|-----|--------|-------------------|------|-------|
| 0   | 1      | [0.1, 0.7, 0.2]   | 1    | 0.7   |
| 1   | 0      | [0.5, 0.25, 0.25] | 0    | 0.5   |

Now the shapes, because `gather` needs an index with as many dimensions as `probs`:

```text
targets          [1, 0]            shape (2,)
as a column      [[1], [0]]        shape (2, 1)
after picking    [[0.7], [0.5]]    shape (2, 1)
drop the 1-axis  [0.7, 0.5]        shape (2,)
```

## Tools you'll need

### tensor.gather(dim, index)

- Picks values along dimension `dim`, using an `index` tensor with the same number of dimensions as the tensor.
- The output has the shape of `index`.
  - For `dim=1` on a 2D tensor: `out[i][j] = t[i][index[i][j]]`.
- Negative dims count from the end, so `-1` is the last dimension.
- The index must be int64.

```python
import torch

t = torch.tensor([[10, 11, 12], [20, 21, 22]])
idx = torch.tensor([[2, 0], [1, 1]])
out = t.gather(1, idx)
print(out)  # tensor([[12, 10], [21, 21]])
print(out.shape)  # torch.Size([2, 2])
```

### tensor.unsqueeze(dim)

- Inserts a new axis of size 1 at position `dim`.
- Use `-1` to add it at the end, which turns `(N,)` into `(N, 1)`.

```python
import torch

v = torch.tensor([5, 6, 7])
print(v.shape)  # torch.Size([3])
print(v.unsqueeze(-1).shape)  # torch.Size([3, 1])
print(v.unsqueeze(0).shape)  # torch.Size([1, 3])
```

### tensor.squeeze(dim)

- The reverse of `unsqueeze`: removes an axis of size 1.
- Pass `dim` explicitly. If that axis is not size 1, nothing happens.
  - Without `dim`, every size-1 axis goes, which can remove ones you wanted to keep.

```python
import torch

m = torch.zeros(4, 1)
print(m.squeeze(-1).shape)  # torch.Size([4])
print(m.squeeze(0).shape)  # torch.Size([4, 1])
```

### Alternative: advanced indexing

- Indexing with integer tensors also picks elements, as in `t[rows, cols]`.
- With many leading dimensions it gets awkward, because you must build an index for every leading axis.
- `gather` handles any number of leading dimensions without extra work.

```python
import torch

t = torch.tensor([[1, 2, 3], [4, 5, 6]])
rows = torch.tensor([0, 1])
cols = torch.tensor([2, 0])
print(t[rows, cols])  # tensor([3, 4])
```

## Common mistakes

- **Forgetting the extra axis.** `gather` errors out if the index has fewer dimensions than `probs`.
  - Add a trailing size-1 axis to the targets first.
- **Gathering along the wrong dim.** The classes are the last axis, so use `-1`, not `0`.
  - A hard-coded `1` breaks when there are extra leading dimensions; `-1` works for any rank.
- **Leaving the extra axis on the output.** After `gather` the shape is `(..., 1)`, but the answer must match `targets.shape`.
  - Remove that axis at the end.
- **Wrong index dtype.** `gather` needs int64 indices, so float or int32 targets raise an error.
- **Using a Python loop.** The problem forbids it, and it is slow on big batches.
  - Let one tensor operation handle all positions at once.

## Hints

### Hint 1

- Each example needs one value from its own row of probabilities, chosen by its target.
- `gather` does this, but it wants an index with the same number of dimensions as `probs`.
- So reshape the targets to fit.
- Then pick the values.
- Then reshape the result back to the shape of `targets`.

### Hint 2

- Give `targets` a trailing axis of size 1 with `unsqueeze`: shape goes from `(...,)` to `(..., 1)`.
- Call `gather` on `probs` along the last dim: shape `(..., 1)`.
- Remove the size-1 axis with `squeeze`: shape is now the shape of `targets`.

### Hint 3

- Along the last dim, `gather` computes `out[..., j] = probs[..., index[..., j]]`.
- Your index has only one column (`j = 0`), so each output entry is `probs[idx][targets[idx]]`, exactly the wanted probability.
- Use `-1` for both the gather dim and the squeeze dim, so it works for any number of leading dimensions.
- The final squeeze makes the result match `targets.shape`.
