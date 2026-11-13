# Learn: Scaled Dot-Product Attention

## The idea

- **Attention** lets each position in a sequence build its output as a weighted average of information from other positions.
- The task: for every query, score all keys, turn the scores into weights, and average the values with those weights.
- It shows up in every Transformer, in the training loop and in inference code for language and vision models.
- **Query**: a vector saying "what am I looking for?"
- **Key**: a vector saying "this is what I hold".
- **Value**: the payload attached to each key. The output is a mix of values.
- **Score**: the dot product of a query and a key. A bigger score means a better match.
- **Scaling**: dividing scores by `sqrt(d)` keeps them from growing with the vector size `d`.
- **Softmax**: turns a row of scores into positive weights that sum to 1.
  - Intuition: the biggest score gets the biggest share.
  - Formula: `exp(x_j) / sum(exp(x))`.
- **Mask**: a boolean tensor saying which keys a query may see. Blocked keys must get weight exactly 0.
- **Batched matmul**: `@` treats leading dimensions as a batch and multiplies the last two as matrices.
- Two traps make this problem "Hard":
  - Huge scores, where a naive `exp` overflows to `inf`.
  - Queries with no allowed key, where softmax produces `nan`.

## Work it by hand

Example 1: `q = [1, 0]`, keys `k0 = [1, 0]`, `k1 = [0, 1]`, values `10` and `20`, mask all `True`. Shapes: `B=1, Tq=1, Tk=2, d=2, dv=1`.

| Step | Result | Shape |
|---|---|---|
| Dot products `q·k0`, `q·k1` | `1, 0` | `(1, 1, 2)` |
| Divide by `sqrt(2) ≈ 1.41421` | `0.70711, 0` | `(1, 1, 2)` |
| Apply mask (all `True`) | unchanged | `(1, 1, 2)` |
| `exp` of each | `2.02812, 1` | `(1, 1, 2)` |
| Sum is `3.02812`; divide each | weights `0.66976, 0.33024` | `(1, 1, 2)` |
| Weighted sum of values | `0.66976·10 + 0.33024·20` | `(1, 1, 1)` |

- The result is `6.6976 + 6.6048 ≈ 13.30239`, the expected output.
- The first key scores higher, so its weight is larger and the answer sits closer to 10 than to 20.
- Example 2, query 1: every key is blocked, so there is nothing to average and the output is defined as 0.

## Tools you'll need

### `x.transpose(-2, -1)`
- Swaps two dimensions. Negative indices count from the end.
- `(-2, -1)` swaps the last two and leaves the batch dimension alone.

```python
import torch
a = torch.zeros(2, 5, 3)
print(a.shape)  # torch.Size([2, 5, 3])
print(a.transpose(-2, -1).shape)  # torch.Size([2, 3, 5])
```

### `a @ b` (batched matrix multiply)
- Multiplies the last two dimensions as matrices; leading dimensions are the batch.
- Shapes `(B, n, m) @ (B, m, p)` give `(B, n, p)`.

```python
import torch
x = torch.ones(2, 3, 4)
y = torch.full((2, 4, 1), 2.0)
print((x @ y).shape)  # torch.Size([2, 3, 1])
print((x @ y)[0, :, 0])  # tensor([8., 8., 8.])
```

### `math.sqrt(n)` and tensor division
- Dividing a tensor by a Python number divides every element.
- `q.shape[-1]` gives the size of the last dimension.

```python
import math
import torch
s = torch.tensor([4.0, 8.0])
print(s / math.sqrt(16))  # tensor([1., 2.])
```

### `~mask` and `t.masked_fill(cond, value)`
- `~` flips a boolean tensor.
- `masked_fill` returns a copy where `cond` is `True` is replaced by `value`.
- It fills where the condition is true, so think about which positions you want to block.
- `float("-inf")` is negative infinity.

```python
import torch
t = torch.tensor([1.0, 2.0, 3.0])
flag = torch.tensor([False, True, False])
print(~flag)  # tensor([ True, False,  True])
print(t.masked_fill(flag, 0.0))  # tensor([1., 0., 3.])
print(t.masked_fill(flag, float("-inf")))  # tensor([1., -inf, 3.])
```

### `torch.softmax(t, dim=-1)`
- Turns scores into weights along `dim`.
- It subtracts the row maximum internally, so large scores are safe.
- `-inf` becomes weight 0. A row of only `-inf` gives `nan`.

```python
import torch
print(torch.exp(torch.tensor(1000.0)))  # tensor(inf)
print(torch.softmax(torch.tensor([2000.0, 2000.0, 2000.0]), dim=-1))  # tensor([0.3333, 0.3333, 0.3333])
ninf = float("-inf")
print(torch.softmax(torch.tensor([0.0, 0.0, ninf]), dim=-1))  # tensor([0.5000, 0.5000, 0.0000])
print(torch.softmax(torch.tensor([ninf, ninf]), dim=-1))  # tensor([nan, nan])
print(torch.ones(2, 4).softmax(dim=-1).sum(dim=-1))  # tensor([1., 1.])
```

### `torch.nan_to_num(t, nan=0.0)`
- Replaces `nan` with the number you choose and leaves other values alone.

```python
import torch
t = torch.tensor([float("nan"), 1.5])
print(torch.nan_to_num(t, nan=0.0))  # tensor([0.0000, 1.5000])
```

## Common mistakes

- **Transposing the wrong dimensions.** `k.T` or `transpose(0, 1)` moves the batch dimension. Use `transpose(-2, -1)`.
- **Softmax over the wrong axis.** Weights must sum to 1 over the keys, the last dimension of `(B, Tq, Tk)`. `dim=1` mixes up queries.
- **Writing your own `exp` and sum.** With scores near 10^6 it overflows to `inf` and gives `nan`. Use the built-in softmax.
- **Inverting the mask.** `True` means allowed, but `masked_fill` fills where its condition is true. Block the positions where the mask is false.
- **Ignoring fully masked rows or `mask=None`.** All-`-inf` rows give `nan` weights, and `nan` times anything stays `nan`. Clean the weights before multiplying by `v`, and skip masking when there is no mask.

## Hints

### Hint 1
- Score every query/key pair and scale the scores.
- If a mask is given, make the disallowed pairs impossible to win.
- Turn each row of scores into weights.
- Repair any rows that came out broken.
- Use the weights to combine the values.

### Hint 2
- Scores: batched matmul of `q` with the transposed `k`, divided by the square root of `d`; shape `(B, Tq, Tk)`.
- Masking: `masked_fill` with negative infinity; shape unchanged.
- Weights: `torch.softmax` over the last dimension; shape unchanged.
- Repair: `torch.nan_to_num`; shape unchanged.
- Output: weights `(B, Tq, Tk)` matmul `v` `(B, Tk, dv)` gives `(B, Tq, dv)`.

### Hint 3
- `exp(-inf) = 0`, so a blocked key adds nothing to the softmax sum and gets weight 0.
- The only failure is a query whose keys are all blocked. Every score is `-inf`, softmax computes 0/0, and the row becomes `nan`.
- Replace those `nan` weights with 0 after the softmax. The weighted sum of the values is then 0, as required.
- Apply the masking step only when `mask` is not `None`.
