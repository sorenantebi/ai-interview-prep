---
topic: "PyTorch Training"
difficulty: Medium
---
# Cross-Entropy from Logits

**Topic:** PyTorch Training · **Difficulty:** Medium

## Problem

`logits` has shape `(n, c)`: one row of unnormalised class scores per example. `targets` has shape `(n,)`
and holds the correct class index of each example (int64). Return the mean cross-entropy loss over the
batch, as a 0-dimensional tensor:

`loss = mean_i( -log softmax(logits[i])[targets[i]] )`

Your function must stay correct for very large logits such as `1000.0`, where computing `exp` directly
overflows. Don't use `F.cross_entropy`, `F.log_softmax`, `F.nll_loss` or `nn.CrossEntropyLoss`.

## Examples

**Example 1**
```text
Input: logits = [[2.0, 1.0, 0.1]], targets = [0]
Output: 0.41703
```

**Example 2**
```text
Input: logits = [[1000.0, 0.0], [0.0, 1000.0]], targets = [0, 0]
Output: 500.00000
Explanation: the first example is certain and right (loss 0), the second is certain and wrong (loss 1000).
```

## Constraints

- `1 <= n <= 10^4`, `2 <= c <= 10^3`
- `0 <= targets[i] < c`
- `-10^4 <= logits[i][j] <= 10^4`
