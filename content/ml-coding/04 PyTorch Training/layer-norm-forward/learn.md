# Learn: Layer Norm Forward

## The idea

- The task: rescale each row of `x` on its own so its features have mean 0 and variance 1, then apply a learned scale and shift.
- Think of one row as one example described by `d` numbers. Other rows in the batch play no part.
- The steps in plain words: subtract the row's average, divide by the row's spread, then multiply by `gamma` and add `beta`.
- **Where it shows up:** layer norm sits inside every Transformer block.
  - It keeps activations at a stable scale, so training doesn't blow up.
- **gamma and beta:** learned per-feature parameters of shape `(d,)`.
  - They let the network undo the normalisation where that helps.
- **Variance:** the average squared distance from the mean.
  - **Biased** variance divides by `d`. The "unbiased" version divides by `d - 1`. This problem wants the biased one.
- **Standard deviation:** the square root of the variance. It is the "spread" you divide by.
- **eps:** a tiny number added to the variance before the square root.
  - It stops a constant row (variance 0) from dividing by zero.
- **Broadcasting:** PyTorch stretches size-1 dimensions so shapes that differ can still be combined.
  - An `(n, 1)` tensor combines with an `(n, d)` tensor.
  - A `(d,)` tensor is applied to every row of an `(n, d)` tensor.

## Work it by hand

Example 1: `x = [[1, 2, 3]]` with shape `(1, 3)`, `gamma = [1, 1, 1]`, `beta = [0, 0, 0]`, `eps = 1e-5`.

| Step | Result | Shape |
|---|---|---|
| Row mean: (1+2+3)/3 | `2` | `(1, 1)` |
| Centre: `x - mean` | `[-1, 0, 1]` | `(1, 3)` |
| Squares of the centred values | `[1, 0, 1]` | `(1, 3)` |
| Biased variance: 2/3 | `0.66667` | `(1, 1)` |
| Add eps | `0.66668` | `(1, 1)` |
| Square root | `0.81650` | `(1, 1)` |
| Divide centred row by it | `[-1.22474, 0, 1.22474]` | `(1, 3)` |
| Multiply by `gamma` (all 1) | `[-1.22474, 0, 1.22474]` | `(1, 3)` |
| Add `beta` (all 0) | `[-1.22474, 0.00000, 1.22474]` | `(1, 3)` |

- The last row is the expected output.
- Sanity check on Example 2: the first row `[2, 2]` centres to `[0, 0]`, so only `beta` is left.
  - That is why its output is `[0.5, -0.5]`.

## Tools you'll need

### `t.mean(dim=-1, keepdim=True)`
- Averages over one dimension. `dim=-1` means the last one, which here is the features.
- `keepdim=True` keeps that dimension with size 1 instead of removing it, so the result still broadcasts against the original.

```python
import torch
a = torch.tensor([[1.0, 3.0], [5.0, 9.0]])
print(a.mean(dim=-1).shape)  # torch.Size([2])
print(a.mean(dim=-1, keepdim=True).shape)  # torch.Size([2, 1])
print(a.mean(dim=-1, keepdim=True))  # tensor([[2.], [7.]])
```

### `t.var(dim=-1, unbiased=False, keepdim=True)`
- Variance along a dimension. By default PyTorch divides by `d - 1`.
- Pass `unbiased=False` to divide by `d`. It accepts `keepdim` just like `mean`.

```python
import torch
b = torch.tensor([[2.0, 4.0, 6.0]])
print(b.var(dim=-1))  # tensor([4.])
print(b.var(dim=-1, unbiased=False))  # tensor([2.6667])
```

### `torch.sqrt(t)`
- Element-wise square root.
- Returns a new tensor of the same shape.

```python
import torch
print(torch.sqrt(torch.tensor([4.0, 9.0])))  # tensor([2., 3.])
```

### Broadcasting with `*`, `-`, `/`, `+`
- Operators line up shapes from the right, and size-1 dimensions stretch.
- An `(n, 1)` tensor works against `(n, d)`. A `(d,)` tensor is applied to every row.

```python
import torch
m = torch.tensor([[1.0], [2.0]])
g = torch.tensor([10.0, 20.0, 30.0])
print((m * g).shape)  # torch.Size([2, 3])
print((m * g)[1])  # tensor([20., 40., 60.])
```

## Common mistakes

- **Wrong dimension.** Reducing over `dim=0` normalises each feature across the batch (that's batch norm).
  - Layer norm reduces over `dim=-1`.
- **Forgetting `keepdim=True`.** A mean of shape `(n,)` doesn't line up with an `(n, d)` tensor.
  - It broadcasts against the wrong dimension or raises an error. Keep the `(n, 1)` shape.
- **Unbiased variance.** `var` divides by `d - 1` by default.
  - Example 1 would give `1.0` instead of `0.6667`, and the output would be wrong.
- **eps in the wrong place.** It goes inside the root: `sqrt(var + eps)`, not `sqrt(var) + eps`.
- **Using the forbidden helpers.** `F.layer_norm` and `nn.LayerNorm` are not allowed.
  - Build it from `mean`, `var` and arithmetic.

## Hints

### Hint 1
- Work on every row independently, but all at once.
- Find each row's mean and its biased variance.
- Subtract the mean from the row.
- Divide by the square root of the variance plus `eps`.
- Multiply by the per-feature scale, then add the per-feature shift.

### Hint 2
- Take the mean over the last dimension with `keepdim=True`: shape `(n, 1)`.
- Take the variance the same way with `unbiased=False`: shape `(n, 1)`.
- Use `torch.sqrt` on the variance plus `eps` for the denominator: shape `(n, 1)`.
- The normalised result has shape `(n, d)`.
- `gamma` and `beta` of shape `(d,)` broadcast across its rows.

### Hint 3
- For each row `i`, the normalised value is `(x[i] - mean_i) / sqrt(var_i + eps)`.
- Then multiply that whole row element-wise by `gamma` and add `beta`.
- Because the statistics have shape `(n, 1)`, one expression over the whole tensor does it all.
- No loop over rows is needed.
