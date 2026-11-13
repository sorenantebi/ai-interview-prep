# Learn: Batched Pairwise Distances

## The idea

- **Task:** for every point in `a` and every point in `b` (same batch item), measure the straight-line distance between them.
  - `a` is `(B, N, D)`, `b` is `(B, M, D)`, and the answer is `(B, N, M)`.
  - Each batch item gives a table with N rows and M columns.
- **Euclidean distance:** the ordinary "ruler" distance, the square root of the sum of squared coordinate differences.
- **Batch:** B independent problems stacked along the first axis. Batch `k` of `a` only meets batch `k` of `b`.
- **Where it shows up:**
  - nearest-neighbour search and retrieval evaluation
  - k-means (distance from points to centroids)
  - contrastive and metric-learning losses
- **Broadcasting:** PyTorch's rule for combining tensors of different shapes. An axis of size 1 is stretched to match the other tensor.
  - `(B, N, 1)` plus `(B, 1, M)` gives `(B, N, M)`.
- **The memory catch:** subtracting every pair directly builds a `(B, N, M, D)` tensor.
  - With B=4, N=500, M=400, D=64 that is about 51 million numbers.
- **The trick:** rewrite the squared distance with algebra so the heavy part becomes one matrix multiply.
  - `||x - y||^2 = ||x||^2 + ||y||^2 - 2 * (x · y)`
  - The squared norms are one number per point.
  - The dot products for all pairs are exactly a matrix product.
- **Matrix multiply:** entry `(i, j)` of the result is the dot product of row `i` of the first matrix with column `j` of the second.
- **NaN:** "not a number", what `sqrt` returns for a negative input.
  - Rounding can make the squared distance of two equal points a tiny negative number, so you must guard against it.

## Work it by hand

Example 1: `a = [[0,0],[3,4]]`, `b = [[0,0],[6,8]]`. So B=1, N=2, M=2, D=2.

1. Squared norms of `a`'s rows: `[0, 25]`.
   - As a column, shape `(1, 2, 1)`.
2. Squared norms of `b`'s rows: `[0, 100]`.
   - As a row, shape `(1, 1, 2)`.
3. Dot products of every `a` row with every `b` row, shape `(1, 2, 2)`:
   - a0·b0 = 0, a0·b1 = 0
   - a1·b0 = 0, a1·b1 = 3·6 + 4·8 = 50
4. Squared distance = norm_a + norm_b - 2·dot. Broadcasting stretches the column and row to `(1, 2, 2)`:

| | b0 | b1 |
|---|---|---|
| a0 | 0 + 0 - 0 = 0 | 0 + 100 - 0 = 100 |
| a1 | 25 + 0 - 0 = 25 | 25 + 100 - 100 = 25 |

5. Clamp anything below 0 up to 0 (nothing changes here).
6. Square root of each entry: `[[0, 10], [5, 5]]`.

Final output: `[[[0.0, 10.0], [5.0, 5.0]]]`, matching the expected result.

## Tools you'll need

### `x.sum(dim, keepdim=False)`

- Adds up values along an axis.
- With `keepdim=True` the summed axis stays with size 1, which helps with broadcasting.

```python
import torch
x = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
print(x.sum(-1).shape)  # torch.Size([2])
print(x.sum(-1, keepdim=True).shape)  # torch.Size([2, 1])
print(x.sum(-1))  # tensor([ 6., 15.])
```

### `x.unsqueeze(dim)` and indexing with `None`

- Inserts a new axis of size 1 at position `dim`.
- This turns a flat list of norms into a row or a column.

```python
import torch
v = torch.tensor([[1., 2., 3.], [4., 5., 6.]])  # shape (2, 3)
print(v.unsqueeze(1).shape)  # torch.Size([2, 1, 3])
print(v[:, :, None].shape)  # torch.Size([2, 3, 1])
```

### Broadcasting

- When shapes differ, size-1 axes stretch to match.
- A `(1, 3, 1)` plus a `(1, 1, 2)` gives `(1, 3, 2)`.

```python
import torch
col = torch.tensor([[[1.], [2.], [3.]]])  # (1, 3, 1)
row = torch.tensor([[[10., 20.]]])  # (1, 1, 2)
print((col + row).shape)  # torch.Size([1, 3, 2])
print(col + row)  # tensor([[[11., 21.], [12., 22.], [13., 23.]]])
```

### `@` and `.transpose(d0, d1)`

- `@` on 3D tensors is a batched matrix multiply: `(B, N, D) @ (B, D, M)` gives `(B, N, M)`.
- `transpose(1, 2)` swaps the last two axes so the shapes line up. Axis 0 (the batch) stays put.

```python
import torch
p = torch.ones(2, 3, 4)
q = torch.ones(2, 5, 4)
print(q.transpose(1, 2).shape)  # torch.Size([2, 4, 5])
print((p @ q.transpose(1, 2)).shape)  # torch.Size([2, 3, 5])
```

### `x.clamp_min(0)` / `torch.clamp(x, min=0)`

- Replaces every value below the limit with the limit.

```python
import torch
x = torch.tensor([-1e-9, 2.0, -3.0])
print(x.clamp_min(0))  # tensor([0., 2., 0.])
```

### `x.sqrt()`

- Element-wise square root.
- A negative input gives `nan`.

```python
import torch
print(torch.tensor([4., 9.]).sqrt())  # tensor([2., 3.])
print(torch.tensor([-1.]).sqrt())  # tensor([nan])
```

## Common mistakes

- **Building the `(B, N, M, D)` difference tensor.** It works on small inputs but uses far too much memory on large ones.
  - Use the norm expansion with a matrix multiply instead.
- **Wrong norm shapes.** The norms of `a` must be a column `(B, N, 1)` and the norms of `b` a row `(B, 1, M)`.
  - If both are columns, you get an error or wrong values. Print `.shape` after each step.
- **Forgetting to clamp.** A squared distance can come out as something like `-1e-16`, and `sqrt` then gives `nan`.
  - Clamp at 0 before the square root, not after.
- **Transposing the wrong axes.** Swap only the last two axes (1 and 2); axis 0 is the batch.
- **Dropping the factor 2 or the minus sign** on the cross term.

## Hints

### Hint 1

- Don't subtract the points directly.
- Compute the squared length of every point in `a`.
- Compute the squared length of every point in `b`.
- Compute the dot product of every `a` point with every `b` point.
- Combine these into a table of squared distances.
- Make sure nothing is negative, then take the square root.

### Hint 2

- Square the inputs and sum over the last axis: shapes `(B, N)` and `(B, M)`.
- Add an axis so they become `(B, N, 1)` and `(B, 1, M)`.
- Dot products: batched matrix multiply of `a` with `b` whose last two axes are swapped, giving `(B, N, M)`.
- Adding the norms and subtracting the scaled dot products broadcasts to `(B, N, M)`.
- Clamp with `clamp_min`, then `sqrt`.

### Hint 3

- For batch k and pair (i, j): squared distance = (squared length of a[k,i]) + (squared length of b[k,j]) - 2 × (dot product of a[k,i] and b[k,j]).
- The first term varies only with i (a column), the second only with j (a row).
- The third term is the matrix multiply result at position (k, i, j).
- After combining, replace any value below 0 with 0.
- Only then take the square root.
