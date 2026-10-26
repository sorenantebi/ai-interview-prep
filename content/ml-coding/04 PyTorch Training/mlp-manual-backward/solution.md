---
topic: "PyTorch Training"
difficulty: Hard
---
# MLP Manual Backward - Solution

## Intuition

Backpropagation applies the chain rule one layer at a time, from the loss back to the input. Each linear layer `out = a @ W.T + b` sends the incoming gradient `g` to its weights as `g.T @ a`, to its bias as the column sums of `g`, and to its input as `g @ W`. ReLU lets the gradient through only where its input was positive.

## Approach

1. Run the forward pass and keep `z1`, `a1` and `out`.
2. `dout = 2 · (out - y) / (n·k)`: the derivative of the mean squared error.
3. Second layer: `dW2 = dout.T @ a1`, `db2 = dout.sum(0)`, `da1 = dout @ W2`.
4. ReLU: `dz1 = da1 * (z1 > 0)`.
5. First layer: `dW1 = dz1.T @ x`, `db1 = dz1.sum(0)`.

## Code

```python
import torch

def mlp_backward(x: torch.Tensor, y: torch.Tensor, W1: torch.Tensor, b1: torch.Tensor, W2: torch.Tensor, b2: torch.Tensor) -> list:
    z1 = x @ W1.T + b1
    a1 = torch.relu(z1)
    out = a1 @ W2.T + b2
    dout = 2 * (out - y) / out.numel()
    dW2 = dout.T @ a1
    db2 = dout.sum(0)
    dz1 = (dout @ W2) * (z1 > 0)
    dW1 = dz1.T @ x
    db1 = dz1.sum(0)
    return [dW1, db1, dW2, db2]
```

## Complexity

- **Time:** `O(n·h·(d + k))` — the same matrix products as the forward pass, twice.
- **Space:** `O(n·(h + k))` — the saved activations and their gradients.
