---
topic: "PyTorch Training"
difficulty: Medium
---
# SGD with Momentum Step

**Topic:** PyTorch Training · **Difficulty:** Medium

## Problem

Implement one step of SGD with momentum and L2 weight decay, using the same update as `torch.optim.SGD`
(with no dampening and no Nesterov):

1. `g = grad + weight_decay · param`
2. `velocity_new = momentum · velocity + g`
3. `param_new = param - lr · velocity_new`

`param`, `grad` and `velocity` all have the same shape. Return `[param_new, velocity_new]` as new tensors,
without modifying the inputs. (Note that PyTorch puts the learning rate outside the velocity, unlike some
textbooks.)

## Examples

**Example 1**
```text
Input: param = [1.0, -2.0], grad = [0.5, 0.5], velocity = [0.0, 0.0], lr = 0.1, momentum = 0.9, weight_decay = 0.0
Output: [[0.95000,-2.05000],[0.50000,0.50000]]
Explanation: with no previous velocity, the step is just lr · grad.
```

**Example 2**
```text
Input: param = [1.0], grad = [0.2], velocity = [1.0], lr = 0.5, momentum = 0.9, weight_decay = 0.1
Output: [[0.40000],[1.20000]]
```

## Constraints

- `param`, `grad` and `velocity` have the same shape, with at least one element.
- `0 < lr <= 10`, `0 <= momentum < 1`, `0 <= weight_decay <= 1`
