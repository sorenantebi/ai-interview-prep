---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Flatten Spatial Dims - Solution

## Intuition

Merging `H` and `W` into one axis is a reshape (they are adjacent and in row-major order). What remains is moving the channel axis last, which is a transpose of two axes.

## Approach

1. `x.flatten(2)` turns `(B, C, H, W)` into `(B, C, H*W)`.
2. `.transpose(1, 2)` swaps to `(B, H*W, C)`. Both are views, so no data is copied.

## Code

```python
import torch

def flatten_spatial(x: torch.Tensor) -> torch.Tensor:
    return x.flatten(2).transpose(1, 2)
```

## Complexity

- **Time:** `O(1)` — flatten and transpose only change the view's strides (O(B·C·H·W) if you later make it contiguous).
- **Space:** `O(1)` — the result is a view of `x`.
