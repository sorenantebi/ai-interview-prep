# Learn: Linear Layer Forward

## The idea

- **Linear (fully connected) layer**: turns a vector of input features into a new vector of output features.
  - Each output is a weighted sum of all the inputs, plus a constant offset.
- The task: compute that layer for a whole batch at once, using only tensor operations.
- It shows up in almost every model's forward pass during training, from tiny classifiers to the feed-forward blocks inside transformers.
- **Weights `W`**: a matrix with one row per output feature, shape `(d_out, d_in)`.
  - Output `j` is the dot product of row `j` of `W` with the input, plus `b[j]`.
- **Bias `b`**: one constant per output feature, shape `(d_out,)`.
- **Batch**: `x` has shape `(n, d_in)`, one example per row.
  - You want all `n` results together, with no Python loop.
- **Dot product**: multiply two vectors entry by entry, then add up the products.
- **Matrix product**: computes many dot products in one go.
  - Entry `[i, k]` is row `i` of the left matrix dotted with column `k` of the right one.
- **Transpose**: flips a matrix so rows become columns.
- **Broadcasting**: PyTorch's rule for combining tensors of different shapes.
  - A smaller tensor is stretched along missing or size-1 dimensions so the shapes match.
  - Here, one bias vector gets reused for every example.

## Work it by hand

Example 1: `x = [[1.0, 2.0]]` (shape `(1, 2)`), `W` has shape `(3, 2)`, `b = [0.0, 1.0, -1.0]`.

1. Pick out the rows of `W`: `(1.0, 0.0)`, `(0.5, -1.0)`, `(2.0, 1.0)`.
2. Dot each row with `x = (1, 2)`:

| Output | Row of W | Dot with x | Add bias | Result |
|---|---|---|---|---|
| 0 | (1.0, 0.0) | 1·1 + 0·2 = 1.0 | + 0.0 | 1.0 |
| 1 | (0.5, -1.0) | 0.5·1 − 1·2 = −1.5 | + 1.0 | −0.5 |
| 2 | (2.0, 1.0) | 2·1 + 1·2 = 4.0 | − 1.0 | 3.0 |

3. Read off the result: `[[1.0, -0.5, 3.0]]`, shape `(1, 3)` = `(n, d_out)`. This matches the expected output.
4. Now check the shapes for a matrix product:
   - `x` is `(n, d_in)` and `W` is `(d_out, d_in)`, so the inner sizes don't line up.
   - Flip `W` to shape `(d_in, d_out)`, so column `j` holds what was row `j`.
   - Then `(n, d_in)` times `(d_in, d_out)` gives `(n, d_out)`.
5. The bias `(d_out,)` is added to every one of the `n` rows.

## Tools you'll need

### Matrix product: `a @ b` (or `torch.matmul(a, b)`)

- For 2-D tensors, `@` takes `(p, q)` and `(q, r)` and returns `(p, r)`.
- The inner sizes `q` must match.

```python
import torch

a = torch.tensor([[1.0, 2.0, 3.0], [0.0, 1.0, 0.0]])  # (2, 3)
c = torch.tensor([[1.0], [10.0], [100.0]])            # (3, 1)
print((a @ c).shape)  # torch.Size([2, 1])
print(a @ c)          # tensor([[321.], [ 10.]])
```

### Transpose: `t.T` (or `t.transpose(0, 1)`)

- Swaps the two dimensions of a 2-D tensor.
- It returns a view: no data is copied and the original is unchanged.

```python
import torch

m = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(m.shape)    # torch.Size([2, 3])
print(m.T.shape)  # torch.Size([3, 2])
print(m.T)        # tensor([[1., 4.], [2., 5.], [3., 6.]])
```

### Broadcasting with `+`

- Adding a `(n, k)` tensor and a `(k,)` tensor lines shapes up from the right.
- The `(k,)` tensor acts as one row repeated for all `n` rows, with no loop or manual copy.

```python
import torch

grid = torch.zeros(3, 2)           # shape (3, 2)
offset = torch.tensor([5.0, 7.0])  # shape (2,)
print((grid + offset).shape)  # torch.Size([3, 2])
print(grid + offset)          # tensor([[5., 7.], [5., 7.], [5., 7.]])
```

## Common mistakes

- **Forgetting the transpose.** `x @ W` fails unless the sizes happen to match.
  - Check that the inner sizes agree before multiplying.
- **Transposing the wrong thing.** Don't transpose `x`.
  - Each row of `x` is one example, and the output must keep `n` rows.
- **Using elementwise `*` instead of `@`.** `*` multiplies matching entries and never sums them.
  - You need the matrix product.
- **Adding the bias along the wrong axis.** `b` must line up with the last axis of the `(n, d_out)` result.
  - Don't reshape it into a column.
- **Using forbidden shortcuts.** `nn.Linear`, `F.linear` and loops are not allowed.
  - Print `.shape` at each step to confirm your plan.

## Hints

### Hint 1
- Compute all dot products between example rows and weight rows with one matrix product.
- Then add the bias to every row of the result.

### Hint 2
- Transpose `W` so it has shape `(d_in, d_out)`.
- Multiply `x` of shape `(n, d_in)` by it to get `(n, d_out)`.
- Add `b` of shape `(d_out,)`; it broadcasts across the rows.

### Hint 3
- Entry `[i, j]` of the result should be the dot product of `x[i]` with row `j` of `W`, plus `b[j]`.
- Multiplying `x` by the transpose of `W` produces exactly those dot products.
- The bias then adds `b[j]` to column `j` in each of the `n` rows.
