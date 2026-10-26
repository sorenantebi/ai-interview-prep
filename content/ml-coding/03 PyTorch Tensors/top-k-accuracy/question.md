---
topic: "PyTorch Tensors"
difficulty: Hard
---
# Top-k Accuracy

**Topic:** PyTorch Tensors · **Difficulty:** Hard

## Problem

`logits` has shape `(N, C)` (float) and `targets` has shape `(N,)` (int64 class indices). A sample counts as correct when its target is among the `k` highest-scoring classes. Ties are resolved in the sample's favour: it is correct when fewer than `k` classes have a logit strictly greater than the target's logit.

Return the fraction of correct samples as a Python `float` (not a tensor). Don't use Python loops over samples.

Careful: `torch.topk` breaks ties arbitrarily, so a solution that checks whether the target is in `topk(...).indices` can be wrong on ties.

## Examples

**Example 1**
```text
Input: logits = [[0.1, 0.5, 0.4], [0.3, 0.2, 0.9]], targets = [2, 1], k = 2
Output: 0.50000
Explanation: Sample 0: only 0.5 beats the target's 0.4, so it's in the top 2. Sample 1: 0.3 and 0.9 both beat 0.2, so it isn't.
```

**Example 2**
```text
Input: logits = [[1.0, 1.0, 1.0]], targets = [2], k = 1
Output: 1.00000
Explanation: All three classes tie, so no class is strictly greater: correct.
```

## Constraints

- `1 <= N <= 10^5`, `1 <= k <= C <= 10^4`
- `0 <= targets[i] < C`
