---
topic: "PyTorch Training"
difficulty: Hard
---
# MLP Manual Backward

**Topic:** PyTorch Training · **Difficulty:** Hard

## Problem

A two-layer network computes

- `z1 = x @ W1.T + b1`, `a1 = relu(z1)`
- `out = a1 @ W2.T + b2`
- `L = mean( (out - y)² )` over all `n·k` elements

with `x` of shape `(n, d)`, `y` of shape `(n, k)`, `W1` of shape `(h, d)`, `b1` of shape `(h,)`, `W2` of shape
`(k, h)` and `b2` of shape `(k,)`. Return the gradients of `L` as `[dW1, db1, dW2, db2]`, each with the
same shape as its parameter.

Derive them by hand with the chain rule: don't call `backward()`, `torch.autograd` or any `nn` module.
Use a ReLU derivative of 0 where `z1 <= 0`.

## Examples

**Example 1**
```text
Input: x = [[1.0, -1.0]], y = [[0.0]], W1 = [[1.0, 0.0], [0.0, 1.0]], b1 = [0.0, 0.0], W2 = [[1.0, 1.0]], b2 = [0.0]
Output: [[[2.00000,-2.00000],[0.00000,0.00000]],[2.00000,0.00000],[[2.00000,0.00000]],[2.00000]]
Explanation: z1 = [1, -1], so only the first hidden unit is active; out = 1 and ∂L/∂out = 2 · (1 - 0) = 2.
```

**Example 2**
```text
Input: x = [[1.0, 2.0], [0.5, -1.0]], y = [[1.0], [0.0]], W1 = [[0.5, -0.5], [1.0, 1.0]], b1 = [0.1, -0.2], W2 = [[1.0, -1.0]], b2 = [0.5]
Output: [[[0.67500,-1.35000],[3.30000,6.60000]],[1.35000,3.30000],[[1.14750,-9.24000]],[-1.95000]]
```

## Constraints

- `1 <= n <= 1000`, `1 <= d, h, k <= 256`
- All tensors are float32.
