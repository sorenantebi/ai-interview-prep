---
topic: "PyTorch Training"
difficulty: Hard
---
# Adam Step - Solution

## Intuition

`m` and `v` are exponential moving averages of the gradient and the squared gradient. They start at 0, so early on they are biased towards 0; dividing by `1 - beta^t` removes that bias. The update divides by `sqrt(v_hat)`, giving each parameter its own step size: about `lr` in the direction of the averaged gradient, smaller where gradients are noisy.

## Approach

1. Update `m` and `v` with their decay rates.
2. Compute the bias-corrected `m_hat` and `v_hat` using `t`.
3. Step the parameter by `lr · m_hat / (sqrt(v_hat) + eps)`.
4. Return the new parameter and the new (uncorrected) `m` and `v`; the corrected values are only used for the step.

## Code

```python
import torch

def adam_step(param: torch.Tensor, grad: torch.Tensor, m: torch.Tensor, v: torch.Tensor, t: int, lr: float,
              beta1: float, beta2: float, eps: float) -> list:
    m = beta1 * m + (1 - beta1) * grad
    v = beta2 * v + (1 - beta2) * grad ** 2
    m_hat = m / (1 - beta1 ** t)
    v_hat = v / (1 - beta2 ** t)
    return [param - lr * m_hat / (torch.sqrt(v_hat) + eps), m, v]
```

## Complexity

- **Time:** `O(N)` — for `N` parameters.
- **Space:** `O(N)` — the new state and parameter tensors.
