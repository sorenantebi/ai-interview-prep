---
topic: "PyTorch Training"
difficulty: Easy
---
# MSE Loss - Solution

## Intuition

The loss averages one number per element, so the shape doesn't matter: square the element-wise difference and take the mean over everything.

## Approach

1. Compute `diff = pred - target`.
2. Return `(diff ** 2).mean()`, which averages over all elements and gives a 0-dimensional tensor.

## Code

```python
import torch

def mse_loss(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    return ((pred - target) ** 2).mean()
```

## Complexity

- **Time:** `O(N)` — for `N` elements.
- **Space:** `O(N)` — the difference tensor.
