---
topic: "PyTorch Training"
difficulty: Medium
---
# Clip Gradient Norm

**Topic:** PyTorch Training · **Difficulty:** Medium

## Problem

Gradient clipping rescales a model's gradients when they get too large. `grads` is a list of gradient
tensors, one per parameter, possibly of different shapes. Compute the *total* L2 norm over every element
of every tensor:

`total = sqrt( Σ_tensors Σ_elements g² )`

then, like `torch.nn.utils.clip_grad_norm_`, compute `coef = max_norm / (total + 1e-6)`. If `coef < 1`,
multiply every gradient by `coef`; otherwise leave them unchanged. Return the list of resulting gradients
in the same order, as new tensors; don't modify the inputs.

(In the examples every gradient has the same shape so they fit on one line, but your function must accept
gradients of different shapes.)

## Examples

**Example 1**
```text
Input: grads = [[3.0, 4.0]], max_norm = 1.0
Output: [[0.60000,0.80000]]
Explanation: the total norm is 5, so everything is scaled by about 1 / 5.
```

**Example 2**
```text
Input: grads = [[1.0, 0.0], [0.0, 1.0]], max_norm = 5.0
Output: [[1.00000,0.00000],[0.00000,1.00000]]
Explanation: the total norm is about 1.414, already below 5, so nothing changes.
```

**Example 3**
```text
Input: grads = [[6.0], [8.0]], max_norm = 5.0
Output: [[3.00000],[4.00000]]
Explanation: the norm is taken over all tensors together: sqrt(36 + 64) = 10.
```

## Constraints

- `1 <= len(grads) <= 100`, each tensor has at least one element.
- `0 < max_norm <= 10^3`
