---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Flatten Spatial Dims

**Topic:** PyTorch Tensors · **Difficulty:** Easy

## Problem

A convolutional feature map `x` has shape `(B, C, H, W)`. A transformer wants it as a sequence of tokens instead: return a tensor of shape `(B, H*W, C)` where token `t = h*W + w` holds the `C` channel values at grid position `(h, w)` (row-major over the grid).

Keep the input's dtype and don't use Python loops.

## Examples

**Example 1**
```text
Input: x = [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]]
Output: [[[1,5],[2,6],[3,7],[4,8]]]
Explanation: B=1, C=2, H=W=2. Token 0 is position (0, 0), whose two channels hold 1 and 5.
```

**Example 2**
```text
Input: x = [[[[1, 2, 3]]], [[[4, 5, 6]]]]
Output: [[[1],[2],[3]],[[4],[5],[6]]]
```

## Constraints

- `x.dim() == 4`
- `1 <= B, C, H, W <= 512`
