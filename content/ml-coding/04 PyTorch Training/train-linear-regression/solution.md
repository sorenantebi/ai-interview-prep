---
topic: "PyTorch Training"
difficulty: Medium
---
# Train Linear Regression - Solution

## Intuition

Gradient descent repeats one thing: compute the loss on all data, find which direction increases it, and move the parameters a little the other way. Autograd computes `∂L/∂w` and `∂L/∂b` for you; by hand they are `(2/n) Xᵀ r` and `(2/n) Σ r` for the residuals `r = pred - y`.

## Approach

1. Copy `w` and turn `b` into a tensor, both with `requires_grad=True`.
2. Create `torch.optim.SGD([w, b], lr=lr)`.
3. Repeat `steps` times: zero the gradients, compute the loss, call `backward()`, call `opt.step()`.
4. Return the detached `w` and `b`.

## Code

```python
import torch

def train_linear_regression(X: torch.Tensor, y: torch.Tensor, w: torch.Tensor, b: float, lr: float, steps: int) -> list:
    w = w.detach().clone().requires_grad_(True)
    b = torch.tensor(float(b), requires_grad=True)
    opt = torch.optim.SGD([w, b], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        loss = ((X @ w + b - y) ** 2).mean()
        loss.backward()
        opt.step()
    return [w.detach(), b.detach()]
```

## Complexity

- **Time:** `O(steps·n·d)` — each step is a forward and backward pass over all data.
- **Space:** `O(n + d)` — the predictions, residuals and gradients.
