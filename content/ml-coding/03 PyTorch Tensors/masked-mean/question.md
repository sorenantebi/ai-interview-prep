---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Masked Mean

**Topic:** PyTorch Tensors · **Difficulty:** Easy

## Problem

A batch of padded sequences `x` has shape `(B, T, D)` (float). `mask` has shape `(B, T)` and holds integers: `1` for a real token and `0` for padding. Padded positions of `x` hold arbitrary finite values.

Return a float tensor of shape `(B, D)`: for each sequence, the mean of `x[b, t]` over the positions where `mask[b, t] == 1`. If a sequence has no real tokens, its row is all zeros. Don't use Python loops.

## Examples

**Example 1**
```text
Input: x = [[[1.0, 2.0], [3.0, 4.0], [100.0, 100.0]]], mask = [[1, 1, 0]]
Output: [[2.00000,3.00000]]
Explanation: The padded third token (100, 100) is ignored: mean of (1, 2) and (3, 4).
```

**Example 2**
```text
Input: x = [[[1.0], [2.0]], [[5.0], [7.0]]], mask = [[0, 0], [1, 1]]
Output: [[0.00000],[6.00000]]
Explanation: The first sequence is all padding, so its row is 0.
```

## Constraints

- `1 <= B, T, D <= 1024`
- `mask[b][t]` is 0 or 1
- Padded values of `x` are finite but can be huge
