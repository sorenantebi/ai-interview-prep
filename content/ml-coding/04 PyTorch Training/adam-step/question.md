---
topic: "PyTorch Training"
difficulty: Hard
---
# Adam Step

**Topic:** PyTorch Training · **Difficulty:** Hard

## Problem

Implement one Adam update. You get the parameter, its gradient, the optimiser state `m` (first moment)
and `v` (second moment) from the previous step, and the number `t` of *this* step (the first step is
`t = 1`). Compute:

1. `m_new = beta1 · m + (1 - beta1) · grad`
2. `v_new = beta2 · v + (1 - beta2) · grad²`
3. `m_hat = m_new / (1 - beta1^t)` and `v_hat = v_new / (1 - beta2^t)` (bias correction)
4. `param_new = param - lr · m_hat / (sqrt(v_hat) + eps)`

All tensors have the same shape. Return `[param_new, m_new, v_new]` as new tensors, without modifying the
inputs. This matches `torch.optim.Adam` without weight decay.

## Examples

**Example 1**
```text
Input: param = [1.0, 2.0], grad = [0.1, -0.2], m = [0.0, 0.0], v = [0.0, 0.0], t = 1, lr = 0.001, beta1 = 0.9, beta2 = 0.999, eps = 1e-8
Output: [[0.99900,2.00100],[0.01000,-0.02000],[0.00001,0.00004]]
Explanation: on the first step bias correction makes m_hat = grad and v_hat = grad², so each parameter moves by about lr against the sign of its gradient.
```

**Example 2**
```text
Input: param = [0.5], grad = [1.0], m = [0.2], v = [0.05], t = 10, lr = 0.01, beta1 = 0.9, beta2 = 0.999, eps = 1e-8
Output: [[0.49810],[0.28000],[0.05095]]
```

## Constraints

- All tensors have the same shape, with at least one element; `v >= 0`.
- `1 <= t <= 10^6`
- `0 < lr <= 1`, `0 <= beta1, beta2 < 1`, `0 < eps <= 1e-3`
