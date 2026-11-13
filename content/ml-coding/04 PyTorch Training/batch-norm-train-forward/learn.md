# Learn: Batch Norm Training Forward

## The idea

- **Batch normalisation** rescales each feature so that, across the current batch, it has mean 0 and variance 1.
- Then it applies a learnable scale (`gamma`) and shift (`beta`), so the network can undo the normalisation if that helps.
- The task: compute per-feature batch statistics, normalise `x`, and return updated running statistics.
- It shows up inside neural networks, usually between a linear layer and its activation.
  - It keeps values in a stable range, so training is faster and steadier.
- **Per feature**: each column of `x` is handled on its own.
  - With `x` of shape `(n, d)` you compute `d` means and `d` variances, running down the rows (`dim=0`).
- **Biased variance**: sum of squared deviations divided by `n`.
  - `y` uses this one, because it describes exactly this batch.
- **Unbiased variance** (Bessel's correction): divided by `n - 1`.
  - The running statistics estimate the whole population for later use, so they use this one, as `nn.BatchNorm1d` does.
- **Running statistics**: a moving average of the batch statistics, used later at inference time.
- **`momentum`**: how much weight the new batch gets.
  - `0.1` means 10% new, 90% old.
- **`eps`**: a tiny number added inside the square root so you never divide by zero.
- **Broadcasting**: a `(d,)` tensor combined with an `(n, d)` tensor is lined up with the last dimension and repeated across every row.

## Work it by hand

Example 1: `x = [[1, 2], [3, 6]]`, so `n = 2`, `d = 2`. `gamma = [1, 1]`, `beta = [0, 0]`, `running_mean = [0, 0]`, `running_var = [1, 1]`, `momentum = 0.1`, `eps = 1e-5`.

| Step | Feature 0 | Feature 1 | Shape |
|---|---|---|---|
| Batch mean `μ` | (1+3)/2 = 2 | (2+6)/2 = 4 | `(2,)` |
| Deviations `x - μ` | -1, 1 | -2, 2 | `(2, 2)` |
| Sum of squared deviations | 1+1 = 2 | 4+4 = 8 | `(2,)` |
| Biased var (÷ n = 2) | 1 | 4 | `(2,)` |
| Unbiased var (÷ n-1 = 1) | 2 | 8 | `(2,)` |
| `sqrt(biased var + eps)` | sqrt(1.00001) ≈ 1.000005 | sqrt(4.00001) ≈ 2.0000025 | `(2,)` |

1. Normalise feature 0: -1/1.000005 ≈ -0.99999 and 1/1.000005 ≈ 0.99999.
2. Normalise feature 1: -2/2.0000025 ≈ -1.00000 and 1.00000.
3. Apply `gamma = 1` and `beta = 0`, which leaves `y` unchanged:

```text
y = [[-0.99999, -1.00000], [0.99999, 1.00000]]
```

4. Running mean: `0.9 · [0, 0] + 0.1 · [2, 4] = [0.2, 0.4]`.
5. Running var, using the unbiased values: `0.9 · [1, 1] + 0.1 · [2, 8] = [1.1, 1.7]`.
6. Final answer: `[y, [0.2, 0.4], [1.1, 1.7]]`, which matches the expected output.

## Tools you'll need

### `t.mean(dim=0)`

- Averages over the given dimension and removes it.
- For shape `(n, d)` with `dim=0`, you get shape `(d,)`.

```python
import torch
t = torch.tensor([[1.0, 10.0], [3.0, 20.0], [5.0, 30.0]])
print(t.mean(dim=0))  # tensor([ 3., 20.])
print(t.mean(dim=0).shape)  # torch.Size([2])
```

### `t.var(dim=0, unbiased=...)`

- Variance along a dimension.
- `unbiased=True` (the default) divides by `n - 1`; `unbiased=False` divides by `n`.
- Newer PyTorch also accepts `correction=1` or `correction=0` for the same purpose.

```python
import torch
t = torch.tensor([[1.0], [2.0], [6.0]])
print(t.var(dim=0, unbiased=False))  # tensor([4.6667])
print(t.var(dim=0, unbiased=True))   # tensor([7.])
```

### Broadcasting

- A `(d,)` tensor combined with an `(n, d)` tensor is matched to the last dimension and repeated for every row.
- So `x - mean` subtracts each feature's mean from its own column, with no loop.

```python
import torch
a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([10.0, 100.0])
print(a * b)  # tensor([[ 10., 200.],
              #         [ 30., 400.]])
print((a * b).shape)  # torch.Size([2, 2])
```

### `torch.sqrt(t)`

- Element-wise square root.
- Returns a new tensor of the same shape.

```python
import torch
v = torch.tensor([4.0, 9.0, 2.25])
print(torch.sqrt(v))  # tensor([2.0000, 3.0000, 1.5000])
```

### Building new tensors instead of modifying inputs

- Ordinary arithmetic like `a * 0.5 + b * 0.5` builds a new tensor and leaves `a` and `b` alone.
- In-place forms (`a.mul_(0.5)`, `a += b`) change the original, so avoid them on the inputs.

```python
import torch
old = torch.tensor([1.0, 2.0])
new = old * 0.9 + torch.tensor([10.0, 10.0]) * 0.1
print(new)  # tensor([1.9000, 2.8000])
print(old)  # tensor([1., 2.])
```

## Common mistakes

- **Wrong dimension.** Statistics go down the batch, `dim=0`.
  - `dim=1` normalises each sample across its features instead (that is layer norm).
- **Mixing up the two variances.** `y` uses the biased variance (÷ `n`); the running update uses the unbiased one (÷ `n - 1`).
  - Use `unbiased=False` for one and `unbiased=True` for the other.
- **Misplacing `eps`.** It goes inside the root: `sqrt(var + eps)`, not `sqrt(var) + eps`.
- **Swapping the momentum weights.** `momentum` multiplies the *new* batch statistic; `1 - momentum` multiplies the *old* running value.
- **Modifying inputs in place.** `running_mean.mul_(...)` or `+=` on an input changes the caller's tensor.
  - Build new tensors instead.

## Hints

### Hint 1
- Compute the per-feature mean and the biased variance over the batch.
- Normalise `x` with them, then apply `gamma` and `beta`.
- Compute the unbiased variance.
- Blend the batch mean and unbiased variance into the running values using `momentum`.
- Return the three results in a list.

### Hint 2
- Take the mean with `x.mean(dim=0)`: shape `(d,)`.
- Take the biased variance with `x.var(dim=0, unbiased=False)`: shape `(d,)`.
- Combine `(n, d)` with `(d,)` by broadcasting, so `y` stays `(n, d)`.
- Take the unbiased variance with `x.var(dim=0, unbiased=True)`: shape `(d,)`.
- Blend with plain arithmetic, giving new `(d,)` tensors.

### Hint 3
- Normalised value: `(x - mean)` divided by the square root of `(biased var + eps)`, then multiplied by `gamma` and added to `beta`.
- Each running statistic is `(1 - momentum)` times its old value plus `momentum` times the new batch value.
  - For the mean, the new value is `μ`.
  - For the variance, the new value is the unbiased variance `s²`.
- Check against Example 1: the running variance should be `[1.1, 1.7]`.
