---
topic: "PyTorch Training"
difficulty: Easy
---
# Inverted Dropout with a Mask

**Topic:** PyTorch Training · **Difficulty:** Easy

## Problem

Dropout zeroes each activation with probability `p` during training. *Inverted* dropout also divides the
surviving activations by `1 - p`, so the expected value of every activation stays the same and nothing
needs to change at inference time.

To keep the result deterministic, the random part is done for you: `mask` has the same shape as `x` and
holds `1.0` for activations that survive and `0.0` for dropped ones. Return the training-time output of
inverted dropout for drop probability `p`. Return a new tensor; don't modify `x`.

## Examples

**Example 1**
```text
Input: x = [1.0, 2.0, 3.0, 4.0], mask = [1.0, 0.0, 1.0, 0.0], p = 0.5
Output: [2.00000,0.00000,6.00000,0.00000]
Explanation: survivors are scaled by 1 / (1 - 0.5) = 2.
```

**Example 2**
```text
Input: x = [[1.0, -2.0], [0.5, 4.0]], mask = [[1.0, 1.0], [0.0, 1.0]], p = 0.2
Output: [[1.25000,-2.50000],[0.00000,5.00000]]
```

## Constraints

- `0 <= p < 1`
- `mask` has the same shape as `x` and contains only `0.0` and `1.0`.
