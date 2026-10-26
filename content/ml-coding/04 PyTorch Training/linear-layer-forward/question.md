---
topic: "PyTorch Training"
difficulty: Easy
---
# Linear Layer Forward

**Topic:** PyTorch Training · **Difficulty:** Easy

## Problem

A fully connected layer maps every input row `x_i` to `W x_i + b`. Given a batch `x` of shape `(n, d_in)`,
a weight matrix `W` of shape `(d_out, d_in)` (the layout `nn.Linear` uses: one row per output feature) and a
bias `b` of shape `(d_out,)`, return the layer's output, of shape `(n, d_out)`.

Use tensor operations only: no `nn.Linear`, no `F.linear` and no Python loops.

## Examples

**Example 1**
```text
Input: x = [[1.0, 2.0]], W = [[1.0, 0.0], [0.5, -1.0], [2.0, 1.0]], b = [0.0, 1.0, -1.0]
Output: [[1.00000,-0.50000,3.00000]]
Explanation: each output is one row of W dotted with x, plus that row's bias.
```

**Example 2**
```text
Input: x = [[0.0, 0.0], [1.0, -1.0]], W = [[2.0, 3.0]], b = [0.5]
Output: [[0.50000],[-0.50000]]
```

## Constraints

- `1 <= n, d_in, d_out <= 1024`
- All tensors are float32.
