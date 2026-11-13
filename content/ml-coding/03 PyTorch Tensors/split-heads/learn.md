# Learn: Split and Merge Heads

## The idea

- The task is to **regroup** the features of each token into `num_heads` equal slices, and to undo that regrouping later.
- No number changes. Only the way the numbers are grouped into axes changes.
- In ML this runs in every Transformer layer, in training and in inference: split before attention, merge after.
- **Multi-head attention**: the model looks at the same sequence several times in parallel, and each "head" works on its own slice of the features.
- **Tensor**: an n-dimensional array. Its **shape** is the size of each axis.
- The letters in the shapes:
  - `B` is the batch size (how many sequences).
  - `T` is the number of tokens per sequence.
  - `D` is the number of features per token.
  - `dh` is one head's slice size, `D / num_heads`.
- **Reshape**: reads the same flat row of numbers with different axis sizes. It does not move data between axes.
- **Transpose**: swaps two axes, so it does change which axis is which.
- **View**: a tensor that shares memory with another one, so no copy is made.
- **Contiguous**: the elements sit in memory in the same order you read them. A transpose usually breaks this.
- Heads must end up in front of the token axis, so you need both a reshape and a transpose.

## Work it by hand

Example 1: `x = [[[1, 2, 3, 4], [5, 6, 7, 8]]]`, `num_heads = 2`, `split = True`.

- Shape of `x` is `(1, 2, 4)`: one sequence, two tokens, four features.
- `dh = 4 / 2 = 2`.

| Step | Result | Shape |
|---|---|---|
| Start | `[[[1,2,3,4],[5,6,7,8]]]` | `(1, 2, 4)` as `(B, T, D)` |
| Cut each token's 4 features into 2 groups of 2 | token 0: `[[1,2],[3,4]]`, token 1: `[[5,6],[7,8]]` | `(1, 2, 2, 2)` as `(B, T, heads, dh)` |
| Swap the token axis and the head axis | head 0: `[[1,2],[5,6]]`, head 1: `[[3,4],[7,8]]` | `(1, 2, 2, 2)` as `(B, heads, T, dh)` |

- Final output: `[[[[1,2],[5,6]],[[3,4],[7,8]]]]`, which matches the expected output.
- The shape looks the same at the end because `T` and `num_heads` are both 2. The meaning of the axes differs.
- In general the shapes go `(B, T, D)` → `(B, T, heads, dh)` → `(B, heads, T, dh)`.
- Merging runs the steps backwards: swap the axes back, then flatten the last two axes into one.

## Tools you'll need

### tensor.reshape(*shape)

- Reads the same numbers with new axis sizes. The total element count must stay the same.
- One size may be `-1`, meaning "work it out".
- The last axis varies fastest, so splitting the last axis keeps neighbouring values together.

```python
import torch

a = torch.arange(6)
print(a.reshape(2, 3).tolist())  # [[0, 1, 2], [3, 4, 5]]
print(a.reshape(3, -1).shape)  # torch.Size([3, 2])
```

### tensor.transpose(dim0, dim1)

- Swaps two axes and leaves the others alone.
- Returns a view: nothing is copied, so the result is often non-contiguous.

```python
import torch

a = torch.zeros(2, 3, 4)
b = a.transpose(0, 2)
print(b.shape)  # torch.Size([4, 3, 2])
print(b.is_contiguous())  # False
```

### reshape vs view

- `view` needs a memory layout that allows the new shape, and raises an error otherwise.
- `reshape` returns a view when it can and quietly copies when it must.
- `.contiguous()` forces a copy into normal order.

```python
import torch

a = torch.arange(6).reshape(2, 3).transpose(0, 1)
print(a.reshape(6).tolist())  # [0, 3, 1, 4, 2, 5]
try:
    a.view(6)
except RuntimeError:
    print("view failed")  # view failed
```

### tensor.shape

- Unpack it to get sizes by name, which keeps reshapes readable.

```python
import torch

t = torch.zeros(5, 7, 12)
n, m, k = t.shape
print(n, m, k)  # 5 7 12
```

### torch.equal(a, b)

- Returns `True` if both tensors have the same shape and values. Handy for testing the round trip.

```python
import torch

a = torch.arange(4)
print(torch.equal(a, a.clone()))  # True
print(torch.equal(a, a.flip(0)))  # False
```

## Common mistakes

- **Reshaping straight to `(B, heads, T, dh)`.**
  - Reshape does not move axes, so the data gets scrambled.
  - Reshape to `(B, T, heads, dh)` first, then transpose.
- **Splitting `D` as `(dh, heads)` instead of `(heads, dh)`.**
  - Head `h` must own the contiguous block `h·dh … (h+1)·dh - 1`.
  - So the head axis comes first in the split.
- **Using `view` after `transpose`.**
  - It raises an error on non-contiguous tensors.
  - Use `reshape`, or call `.contiguous()` first.
- **Merging without swapping the axes back.**
  - Flattening `(B, heads, T, dh)` directly mixes tokens and heads.
  - Move heads next to `dh` first.
- **Skipping the round-trip test.**
  - Check that merge(split(x)) equals `x` with `torch.equal` on a random tensor.

## Hints

### Hint 1
- Splitting has two steps: cut the feature axis into groups.
- Then move the group axis in front of the token axis.
- Merging runs the same two steps in reverse order.

### Hint 2
- Split, step 1: reshape `(B, T, D)` into `(B, T, num_heads, dh)`.
- Split, step 2: swap axes 1 and 2 to get `(B, num_heads, T, dh)`.
- Merge, step 1: swap axes 1 and 2 to get `(B, T, num_heads, dh)`.
- Merge, step 2: reshape to `(B, T, num_heads·dh)`.

### Hint 3
- In the split, the new axes are ordered `(heads, dh)` with heads first, so each head owns a contiguous run of `dh` features.
- In the merge, after swapping, the last two axes are `(heads, dh)`.
- Flattening them puts head 0's features first, then head 1's, and so on.
- The swapped tensor is no longer contiguous, so pick the reshaping method that copies when needed.
