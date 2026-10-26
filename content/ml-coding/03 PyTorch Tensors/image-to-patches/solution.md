---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Image to Patches - Solution

## Intuition

Split each spatial axis into (grid index, offset inside the patch) with one reshape: `(B, C, H/p, p, W/p, p)`. Then put the axes in the output's order, grid row, grid column, channel, row offset, column offset, and flatten.

## Approach

1. Reshape to `(B, C, gh, p, gw, p)` with `gh = H/p`, `gw = W/p`.
2. Permute to `(B, gh, gw, C, p, p)`.
3. Reshape to `(B, gh·gw, C·p·p)` (this copies, because the permuted view isn't contiguous).

## Code

```python
import torch

def image_to_patches(images: torch.Tensor, patch: int) -> torch.Tensor:
    B, C, H, W = images.shape
    p = patch
    x = images.reshape(B, C, H // p, p, W // p, p)
    x = x.permute(0, 2, 4, 1, 3, 5)
    return x.reshape(B, (H // p) * (W // p), C * p * p)
```

## Complexity

- **Time:** `O(B·C·H·W)` — the final reshape copies every pixel once.
- **Space:** `O(B·C·H·W)` — the output.
