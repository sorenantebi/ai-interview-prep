---
topic: "PyTorch Training"
difficulty: Easy
---
# Gradient with Autograd - Solution

## Intuition

Autograd records the operations used to compute a scalar and replays them backwards to get its gradient. To use it on an input that doesn't track gradients, work on a copy that does.

## Approach

1. Make a copy of `x` that requires gradients: `x.detach().clone().requires_grad_(True)`.
2. Compute `f` from that copy as a scalar.
3. Call `torch.autograd.grad(f, x)` and return the gradient (it doesn't require grad itself).

## Code

```python
import torch

def grad_f(x: torch.Tensor) -> torch.Tensor:
    x = x.detach().clone().requires_grad_(True)
    f = (x ** 2 * torch.sin(x)).sum() + x.sum() ** 2
    (g,) = torch.autograd.grad(f, x)
    return g
```

## Complexity

- **Time:** `O(N)` — one forward and one backward pass over `N` elements.
- **Space:** `O(N)` — the saved intermediate values.
