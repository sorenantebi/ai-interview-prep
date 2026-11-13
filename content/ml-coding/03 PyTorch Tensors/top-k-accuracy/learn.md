# Learn: Top-k Accuracy

## The idea

- **Task:** for each sample, decide whether the true class is among the model's `k` best guesses, then report the fraction of samples where it is.
- **Where it shows up:** evaluation reports for classifiers with many similar classes, such as "top-5 accuracy" on ImageNet-style benchmarks.
- **Logits:** the raw scores a model outputs, one per class per sample.
  - Bigger means the model favours that class more.
  - They are not probabilities and can be negative.
- **Target:** the index of the true class for a sample.
- **Top-k accuracy:** a softer form of accuracy where near-misses still count.
  - With `k = 1` it is ordinary accuracy.
- **Key idea:** you don't need to sort.
  - Ask instead: how many classes score strictly higher than the true class?
  - If fewer than `k` do, the target is in the top `k`.
- **Ties:** equal scores don't count as "higher", so a tied target gets the benefit of the doubt.
- **Broadcasting:** PyTorch stretches a size-1 axis to match a bigger tensor during an operation.
  - A `(N, 1)` column compared with an `(N, C)` matrix is applied to every column.
- **Vectorised:** the work runs on whole tensors at once, with no Python loop over samples.

## Work it by hand

Example 1, with `k = 2`:

```text
logits  = [[0.1, 0.5, 0.4],
           [0.3, 0.2, 0.9]]      shape (2, 3)
targets = [2, 1]                 shape (2,)
```

1. Find each row's target logit.
   - Row 0: index 2 gives 0.4.
   - Row 1: index 1 gives 0.2.
   - Result: `[[0.4], [0.2]]`, shape `(2, 1)`.
2. Compare every logit with its own row's target logit:

| row | logits | target logit | logit > target |
|---|---|---|---|
| 0 | 0.1, 0.5, 0.4 | 0.4 | F, T, F |
| 1 | 0.3, 0.2, 0.9 | 0.2 | T, F, T |

3. Count the Trues per row: `[1, 2]`, shape `(2,)`.
4. A row is correct when its count is `< k`, i.e. `< 2`: `[True, False]`.
5. Average the flags as numbers: `(1 + 0) / 2 = 0.5`.
6. Expected output: `0.50000`.

## Tools you'll need

### tensor.gather(dim, index)

- Picks values along `dim`, using an index tensor with the same number of dimensions as the input.
- For `dim=1`: `out[i][j] = input[i][index[i][j]]`.
- The output has the shape of `index`.

```python
import torch
x = torch.tensor([[10, 11, 12], [20, 21, 22]])
idx = torch.tensor([[2], [0]])
print(x.gather(1, idx).tolist())  # [[12], [20]]
print(x.gather(1, idx).shape)  # torch.Size([2, 1])
```

### tensor.unsqueeze(dim)

- Inserts a new axis of size 1 at position `dim`.
- Useful here because `gather` needs a 2-D index, but `targets` is 1-D.

```python
import torch
t = torch.tensor([4, 7, 9])
print(t.shape)  # torch.Size([3])
print(t.unsqueeze(1).shape)  # torch.Size([3, 1])
```

### Broadcasting comparison (`>`)

- Comparing `(N, C)` with `(N, 1)` stretches the column across all classes.
- The result is a boolean tensor of shape `(N, C)`.
- Use strict `>`, not `>=`.

```python
import torch
a = torch.tensor([[1.0, 5.0, 3.0], [2.0, 2.0, 8.0]])
col = torch.tensor([[3.0], [2.0]])
print((a > col).tolist())  # [[False, True, False], [False, False, True]]
print((a > col).shape)  # torch.Size([2, 3])
```

### tensor.sum(dim)

- Adds along an axis and removes it.
- Booleans count as 0 and 1, and the result is an integer tensor.

```python
import torch
m = torch.tensor([[True, True, False], [False, False, False]])
print(m.sum(dim=1).tolist())  # [2, 0]
print(m.sum(dim=1).dtype)  # torch.int64
```

### .float(), .mean(), .item()

- `mean` needs floating-point values, so convert booleans with `.float()` first.
- `.item()` turns a one-element tensor into a plain Python number.

```python
import torch
ok = torch.tensor([True, False, True, True])
m = ok.float().mean()
print(m)  # tensor(0.7500)
print(m.item())  # 0.75
```

### torch.topk (and why not to use it here)

- `torch.topk(x, k)` returns the `k` largest values and their indices.
- With tied values, which index it keeps is arbitrary, so "is the target in the indices?" can be wrong on ties.

```python
import torch
v, i = torch.topk(torch.tensor([3.0, 9.0, 5.0]), 2)
print(v.tolist())  # [9.0, 5.0]
print(i.tolist())  # [1, 2]
```

## Common mistakes

- **Using `topk` indices.** Ties break arbitrarily, so a tied target can be dropped.
  - Count strictly greater logits instead.
- **Using `>=` instead of `>`.** That counts the target itself, and every tie, as beating it.
  - Use strict `>`.
- **Wrong index shape for `gather`.** `targets` is `(N,)` but the index must be `(N, 1)`.
  - Use `unsqueeze(1)`, otherwise you get an error or a wrongly broadcast result.
- **Summing over the wrong axis.** You count across classes, so use `dim=1`, not across samples.
- **Returning a tensor, or averaging booleans.** The problem wants a Python `float`.
  - `.mean()` on a bool or int tensor raises an error, so use `.float()` first, then `.item()`.

## Hints

### Hint 1
- Find the logit the model gave the true class in each row.
- For each row, count the classes that scored strictly higher than that value.
- A row is correct when its count is smaller than `k`.
- Return the fraction of correct rows as a Python number.

### Hint 2
- Use `gather` with an `(N, 1)` index to get the target logits, shape `(N, 1)`.
- Compare the `(N, C)` logits with that column. Broadcasting gives an `(N, C)` boolean tensor.
- Sum over `dim=1` to get an `(N,)` count of higher classes.
- Compare the counts with `k` to get an `(N,)` boolean tensor, then average it as floats.

### Hint 3
- For row `i`, let `t` be the logit at column `targets[i]`.
- The count is the number of columns `j` where `logits[i][j] > t`.
- Row `i` is correct exactly when that count is less than `k`.
- The answer is (number of correct rows) / `N`.
- Turn the boolean tensor into floats, take the mean, and convert the result to a Python number.
