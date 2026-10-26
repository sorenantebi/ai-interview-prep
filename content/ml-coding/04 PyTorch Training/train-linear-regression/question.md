---
topic: "PyTorch Training"
difficulty: Medium
---
# Train Linear Regression

**Topic:** PyTorch Training · **Difficulty:** Medium

## Problem

Fit a linear model `pred = X @ w + b` with full-batch gradient descent on the mean squared error

`L(w, b) = mean_i( (X[i] · w + b - y[i])² )`

`X` has shape `(n, d)`, `y` shape `(n,)`, and you start from the given weights `w` (shape `(d,)`) and bias
`b`. Take exactly `steps` updates `w ← w - lr · ∂L/∂w`, `b ← b - lr · ∂L/∂b`, each using the whole
dataset, and return `[w, b]` with `b` as a 0-dimensional tensor. Get the gradients from autograd (with
`torch.optim.SGD` or by hand) or derive them yourself. Don't modify the input `w`.

## Examples

**Example 1**
```text
Input: X = [[1.0], [2.0], [3.0]], y = [2.0, 4.0, 6.0], w = [0.0], b = 0.0, lr = 0.1, steps = 1
Output: [[1.86667],0.80000]
Explanation: ∂L/∂w = (2/3) · Σ x·(pred - y) = -18.67 and ∂L/∂b = -8, so one step gives w ≈ 1.867 and b = 0.8.
```

**Example 2**
```text
Input: X = [[1.0], [2.0], [3.0]], y = [2.0, 4.0, 6.0], w = [0.0], b = 0.0, lr = 0.05, steps = 200
Output: [[1.97112],0.06565]
Explanation: after enough steps the model approaches w = 2, b = 0.
```

**Example 3**
```text
Input: X = [[1.0, 2.0]], y = [1.0], w = [0.5, 0.5], b = 1.0, lr = 0.1, steps = 0
Output: [[0.50000,0.50000],1.00000]
```

## Constraints

- `1 <= n <= 1000`, `1 <= d <= 20`
- `0 <= steps <= 1000`
- `lr` is small enough that training doesn't diverge.
