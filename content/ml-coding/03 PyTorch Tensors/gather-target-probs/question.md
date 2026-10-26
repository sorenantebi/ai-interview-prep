---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Gather Target Probabilities

**Topic:** PyTorch Tensors · **Difficulty:** Easy

## Problem

`probs` holds class probabilities with shape `(..., C)`: any number of leading dimensions, classes last. `targets` holds integer class indices (int64) with exactly the leading shape of `probs`.

Return a tensor with the shape of `targets` where each entry is the probability of its target class: `out[idx] = probs[idx][targets[idx]]`. This is the quantity a negative log-likelihood loss picks out. Don't use Python loops.

## Examples

**Example 1**
```text
Input: probs = [[0.1, 0.7, 0.2], [0.5, 0.25, 0.25]], targets = [1, 0]
Output: [0.70000,0.50000]
```

**Example 2**
```text
Input: probs = [[[0.9, 0.1], [0.3, 0.7]]], targets = [[1, 1]]
Output: [[0.10000,0.70000]]
Explanation: Leading shape (1, 2): one sequence of two tokens.
```

## Constraints

- `probs.dim() >= 2`, `targets.shape == probs.shape[:-1]`
- `0 <= targets[...] < C`
- `1 <= C <= 10^4`
