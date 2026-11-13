# Learn: Cross-Entropy from Logits

## The idea

- The task: turn raw class scores into one loss number that is small when the model is right and large when it is wrong.
- In ML this is the standard loss of a classification training loop. You compute it on each batch, then call `.backward()` on it.
- **Logits**: the raw scores a classifier outputs, one per class per example.
  - They can be any real number, negative or huge.
  - They are not probabilities yet.
- **Softmax**: turns a row of logits into probabilities.
  - Make each score positive with `exp`, then divide by the row total.
  - A bigger logit gives a bigger probability.
- **Cross-entropy**: how surprised the model is by the correct class.
  - Correct class gets probability 0.9: small loss.
  - Correct class gets probability 0.01: large loss.
  - Per example it is `-log(probability of the correct class)`. The batch loss is the mean of these.
- **Overflow**: `exp(1000)` is too big for a float, so it becomes `inf`, and `inf / inf` gives `nan`.
- The fix is algebra, so you never build the probabilities.
  - `-log softmax(z)[t]` equals `logsumexp(z) - z[t]`.
  - **logsumexp**: `log(sum(exp(z)))`.
- **Max-shift trick**: logsumexp stays safe if you subtract the row maximum `m` first.
  - `logsumexp(z) = m + log(sum(exp(z - m)))`.
  - After the shift the biggest value is 0, so `exp` never exceeds 1.

## Work it by hand

Example 1: `logits = [[2.0, 1.0, 0.1]]` (shape `(1, 3)`), `targets = [0]` (shape `(1,)`).

| Step | Value | Shape |
|---|---|---|
| 1. `exp` of each logit | `[7.3891, 2.7183, 1.1052]` | `(1, 3)` |
| 2. sum of those | `11.2125` | `(1,)` |
| 3. `log` of the sum (logsumexp) | `2.41703` | `(1,)` |
| 4. target logit `z[0]` | `2.0` | `(1,)` |
| 5. loss = step 3 - step 4 | `2.41703 - 2.0 = 0.41703` | `(1,)` |
| 6. mean over the batch | `0.41703` | `()` |

- Check with the probability view:
  - Softmax gives `7.3891 / 11.2125 = 0.65902` for class 0.
  - `-log(0.65902) = 0.41703`. Same number.
- With one example the mean is that value, so the output is `0.41703`.
- With `n` examples, step 5 gives shape `(n,)` and step 6 averages it into a 0-dimensional tensor.

## Tools you'll need

### torch.logsumexp(x, dim)

- Computes `log(sum(exp(x)))` along `dim`, using the max-shift trick internally.
- `dim` is removed from the shape unless you pass `keepdim=True`.

```python
import torch
x = torch.zeros(2, 4)
out = torch.logsumexp(x, dim=1)
print(out.shape)  # torch.Size([2])
print(f"{out[0].item():.4f}")  # 1.3863
```

### Why naive exp fails

- In float32, `exp` overflows for inputs above about 88.

```python
import torch
print(torch.exp(torch.tensor([1000.0])))  # tensor([inf])
print(torch.exp(torch.tensor([0.0])))  # tensor([1.])
```

### x.max(dim, keepdim=True)

- Returns a named tuple with `.values` and `.indices`.
- With `keepdim=True` the reduced dimension stays with size 1, so the result broadcasts against the original.
- This is how you would do the max-shift by hand.

```python
import torch
x = torch.tensor([[1., 5., 2.], [7., 3., 4.]])
m = x.max(dim=1, keepdim=True).values
print(m.shape)  # torch.Size([2, 1])
print((x - m)[0])  # tensor([-4.,  0., -3.])
```

### Picking one entry per row

- Advanced indexing: pass a row-index tensor and a column-index tensor of equal length. Pair `i` picks `(rows[i], cols[i])`.
- `gather(1, idx)`: pass a column index of shape `(n, 1)`. The result keeps that shape.

```python
import torch
a = torch.tensor([[10, 11, 12], [20, 21, 22], [30, 31, 32]])
print(a[torch.tensor([0, 2]), torch.tensor([1, 1])])  # tensor([11, 31])
idx = torch.tensor([2, 0, 1])
g = a.gather(1, idx.unsqueeze(1))
print(g.shape)  # torch.Size([3, 1])
print(g.squeeze(1))  # tensor([12, 20, 31])
```

### torch.arange(n)

- Makes `[0, 1, ..., n-1]`.
- It is handy as the row index in advanced indexing.

```python
import torch
print(torch.arange(4))  # tensor([0, 1, 2, 3])
```

### tensor.mean()

- Averages all elements into a 0-dimensional tensor.

```python
import torch
v = torch.tensor([1., 2., 6.])
print(v.mean())  # tensor(3.)
print(v.mean().shape)  # torch.Size([])
```

## Common mistakes

- **Computing softmax, then log.** `exp(1000)` is `inf`, so you get `nan`.
  - Never build the probabilities. Work in log space with logsumexp.
- **Wrong `dim`.** Classes are along dim 1.
  - Reducing over dim 0 mixes different examples and gives shape `(c,)` instead of `(n,)`.
- **Shape mismatch with `gather`.** It needs an index of shape `(n, 1)` and returns `(n, 1)`.
  - If you forget to squeeze, subtracting from an `(n,)` tensor broadcasts into an `(n, n)` matrix. The mean is wrong and no error is raised.
- **Flipping the sign.** The loss is `logsumexp - target logit`, which is never negative.
  - If you see negatives, you subtracted the wrong way round.
- **Returning shape `(1,)` or `(n,)`.** The answer must be 0-dimensional, so take the mean at the end.

## Hints

### Hint 1
- Rewrite the loss so that no probabilities are needed.
- For each row, get one "log of the total" number.
- For each row, get one "score of the correct class" number.
- Subtract the two per row.
- Average over the rows.

### Hint 2
- Use `torch.logsumexp` along the class dimension. The result has shape `(n,)`.
- Select the correct-class logit of every row with indexing or `gather`. This also ends at shape `(n,)`.
- Subtract the two `(n,)` tensors. The result is still `(n,)`.
- Call `.mean()` to reach a 0-dimensional tensor.

### Hint 3
- For row `i`, the loss is `logsumexp(logits[i]) - logits[i][targets[i]]`.
- To select all those entries at once, use the row numbers `0..n-1` as one index and `targets` as the other.
  - Pair `i` then points at `(i, targets[i])`.
- With `gather`, first turn `targets` into a column of shape `(n, 1)`, then squeeze the result back to `(n,)`.
- Check Example 2:
  - Row 0 gives `1000 - 1000 = 0`.
  - Row 1 gives `logsumexp = 1000`, minus the target logit `0`, so `1000`.
  - The mean is `500`.
