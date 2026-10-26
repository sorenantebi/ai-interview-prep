---
topic: "PyTorch Training"
difficulty: Easy
---
# Gradient with Autograd

**Topic:** PyTorch Training · **Difficulty:** Easy

## Problem

Let `f(x) = Σ x_i² · sin(x_i) + (Σ x_i)²`, where both sums run over every element of the tensor `x`.
Return the gradient `∂f/∂x`, a tensor with the same shape as `x`.

Use `torch.autograd` (`backward()` or `torch.autograd.grad`) rather than deriving the formula by hand. The
input `x` does not require gradients, and you must not modify it. Return a plain tensor that does not
require gradients.

## Examples

**Example 1**
```text
Input: x = [1.0, 2.0]
Output: [8.22324,7.97260]
```

**Example 2**
```text
Input: x = [[0.5, -0.5], [3.0, 0.0]]
Output: [[6.69882,6.69882],[-2.06321,6.00000]]
Explanation: f sums over every element, so the shape of x doesn't matter.
```

## Constraints

- `x` is float32 with at least one element.
- `-100 <= x[i] <= 100`
