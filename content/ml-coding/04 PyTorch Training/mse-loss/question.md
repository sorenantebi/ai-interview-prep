---
topic: "PyTorch Training"
difficulty: Easy
---
# MSE Loss

**Topic:** PyTorch Training · **Difficulty:** Easy

## Problem

Return the mean squared error between `pred` and `target`: the average of `(pred - target)²` over every
element. Both tensors have the same shape, which can have any number of dimensions. Return a 0-dimensional
tensor (a scalar).

Don't use `F.mse_loss` or `nn.MSELoss`.

## Examples

**Example 1**
```text
Input: pred = [1.0, 2.0, 3.0], target = [1.0, 2.0, 5.0]
Output: 1.33333
Explanation: only the last element differs, by 2, so the loss is 4 / 3.
```

**Example 2**
```text
Input: pred = [[0.5, -1.0], [2.0, 0.0]], target = [[0.0, -1.0], [1.0, 1.0]]
Output: 0.56250
```

## Constraints

- `pred` and `target` have the same shape, with at least one element.
- Both are float32.
