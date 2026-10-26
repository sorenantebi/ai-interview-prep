---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Batched Pairwise Distances

**Topic:** PyTorch Tensors · **Difficulty:** Medium

## Problem

`a` has shape `(B, N, D)` and `b` has shape `(B, M, D)` (float). For each batch, return the Euclidean distance between every row of `a` and every row of `b`: a tensor of shape `(B, N, M)` with `out[k, i, j] = ||a[k, i] - b[k, j]||`.

Don't use `torch.cdist` (the hidden tests disable it) or Python loops. Inputs can be large (B = 4, N = 500, M = 400, D = 64), so avoid building the full `(B, N, M, D)` difference tensor, and make sure the result is never `nan`.

## Examples

**Example 1**
```text
Input: a = [[[0.0, 0.0], [3.0, 4.0]]], b = [[[0.0, 0.0], [6.0, 8.0]]]
Output: [[[0.00000,10.00000],[5.00000,5.00000]]]
```

**Example 2**
```text
Input: a = [[[1.0]], [[2.0]]], b = [[[4.0], [0.0]], [[2.0], [-1.0]]]
Output: [[[3.00000,1.00000]],[[0.00000,3.00000]]]
Explanation: Two batches, each compared only with its own b.
```

## Constraints

- `1 <= B <= 16`, `1 <= N, M <= 1000`, `1 <= D <= 256`
- The hidden tests use float64 inputs
