---
topic: "ML From Scratch"
difficulty: Medium
---
# Logistic Regression with Gradient Descent

**Topic:** ML From Scratch · **Difficulty:** Medium

## Problem

Train a binary logistic regression model with full-batch gradient descent.

`X` has shape `(n, d)`, `y` has shape `(n,)` with labels 0 or 1, and training starts from weights `w` (shape `(d,)`) and bias `b`. The model predicts `p = sigmoid(X @ w + b)` with `sigmoid(z) = 1 / (1 + exp(-z))`, and the loss is the mean binary cross-entropy.

Each step computes the gradients of the mean loss on all `n` samples:

- `grad_w = Xᵀ (p - y) / n`
- `grad_b = mean(p - y)`

and then updates both at once: `w = w - lr · grad_w`, `b = b - lr · grad_b`.

Run exactly `steps` steps and return `[w, b]`: the final weights as an array of shape `(d,)` and the final bias as a float.

## Examples

**Example 1**
```text
Input: X = [[0.0], [1.0]], y = [0, 1], w = [0.0], b = 0.0, lr = 1.0, steps = 1
Output: [[0.25000],0.00000]
```

**Example 2**
```text
Input: X = [[1.0, 2.0], [2.0, 0.0], [0.0, 1.0]], y = [1, 0, 1], w = [0.1, -0.1], b = 0.5, lr = 0.5, steps = 3
Output: [[-0.32903,0.42086],0.54802]
```

## Constraints

- `1 <= n <= 10^4`
- `1 <= d <= 20`
- `0 <= steps <= 1000`
- `|X @ w + b|` stays below 30 during training, so the plain sigmoid formula doesn't overflow
