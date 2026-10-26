---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Causal Mask

**Topic:** PyTorch Tensors · **Difficulty:** Easy

## Problem

Decoder self-attention must not let a token look at later tokens. Return the additive mask for a sequence of length `t`: a `float32` tensor of shape `(t, t)` where entry `[i, j]` (query `i`, key `j`) is `0.0` when `j <= i` and `-inf` when `j > i`.

Adding it to the attention scores before the softmax gives the future positions zero weight. Don't use Python loops.

## Examples

**Example 1**
```text
Input: t = 3
Output: [[0.00000,-inf,-inf],[0.00000,0.00000,-inf],[0.00000,0.00000,0.00000]]
Explanation: Row i may attend to keys 0..i.
```

**Example 2**
```text
Input: t = 1
Output: [[0.00000]]
```

## Constraints

- `1 <= t <= 4096`
- The result's dtype is `torch.float32`
