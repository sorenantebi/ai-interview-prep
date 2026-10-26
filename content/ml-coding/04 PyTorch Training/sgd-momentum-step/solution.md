---
topic: "PyTorch Training"
difficulty: Medium
---
# SGD with Momentum Step - Solution

## Intuition

Momentum keeps a running sum of past gradients that decays by `momentum` each step, so consistent gradient directions build up speed while noisy ones cancel out. Weight decay is just an extra gradient term pulling each weight towards 0.

## Approach

1. Add the weight-decay term to the gradient.
2. Decay the old velocity and add the gradient.
3. Step the parameter against the new velocity, scaled by `lr`.

## Code

```python
import torch

def sgd_momentum_step(param: torch.Tensor, grad: torch.Tensor, velocity: torch.Tensor, lr: float,
                      momentum: float, weight_decay: float) -> list:
    g = grad + weight_decay * param
    v = momentum * velocity + g
    return [param - lr * v, v]
```

## Complexity

- **Time:** `O(N)` — for `N` parameters.
- **Space:** `O(N)` — the new parameter and velocity tensors.
