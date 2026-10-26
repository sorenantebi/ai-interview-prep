---
topic: "ML From Scratch"
difficulty: Medium
---
# Logistic Regression with Gradient Descent - Solution

## Intuition

For the sigmoid with cross-entropy, the derivative of the loss with respect to the logit is simply `p - y`. The chain rule then gives `Xᵀ(p - y) / n` for the weights and the mean of `p - y` for the bias.

## Approach

1. Copy `w` (as floats) so the caller's array isn't changed, and make `b` a float.
2. Repeat `steps` times: compute `p = sigmoid(X @ w + b)`, the error `p - y`, both gradients, then update `w` and `b` together.
3. Return `[w, b]`.

## Code

```python
import numpy as np

def logistic_regression_gd(X: np.ndarray, y: np.ndarray, w: np.ndarray, b: float, lr: float, steps: int) -> list:
    w = np.array(w, dtype=float)
    b = float(b)
    n = X.shape[0]
    for _ in range(steps):
        p = 1.0 / (1.0 + np.exp(-(X @ w + b)))
        err = p - y
        grad_w = X.T @ err / n
        grad_b = err.mean()
        w = w - lr * grad_w
        b = b - lr * grad_b
    return [w, float(b)]
```

## Complexity

- **Time:** `O(steps·n·d)` — each step does two matrix-vector products.
- **Space:** `O(n + d)` — the predictions and the weights.
