---
topic: "PyTorch Training"
difficulty: Medium
---
# Clip Gradient Norm - Solution

## Intuition

Clipping by the total norm keeps the gradient's direction across all parameters and only shortens it. Clipping each tensor separately would change that direction, which is why the norm is computed over everything at once.

## Approach

1. Sum the squared entries of every tensor and take the square root: the total norm.
2. Compute `coef = max_norm / (total + 1e-6)`.
3. If `coef < 1`, return each gradient times `coef`; otherwise return copies of the gradients.

## Code

```python
import torch

def clip_grad_norm(grads: list[torch.Tensor], max_norm: float) -> list:
    total = torch.sqrt(sum((g ** 2).sum() for g in grads))
    coef = max_norm / (total + 1e-6)
    if coef < 1:
        return [g * coef for g in grads]
    return [g.clone() for g in grads]
```

## Complexity

- **Time:** `O(N)` — for `N` gradient entries in total.
- **Space:** `O(N)` — the returned gradients.
