---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Split and Merge Heads - Solution

## Intuition

Splitting `D` into `(num_heads, dh)` is a reshape, because a head's features are contiguous. The head axis then moves in front of time with a transpose. Merging undoes the two steps in reverse order.

## Approach

1. Split: `x.reshape(B, T, num_heads, dh).transpose(1, 2)`.
2. Merge: `x.transpose(1, 2).reshape(B, T, num_heads * dh)` (`reshape` copies when the transposed view isn't contiguous; `view` would fail).

## Code

```python
import torch

def regroup_heads(x: torch.Tensor, num_heads: int, split: bool) -> torch.Tensor:
    if split:
        B, T, D = x.shape
        return x.reshape(B, T, num_heads, D // num_heads).transpose(1, 2)
    B, H, T, dh = x.shape
    return x.transpose(1, 2).reshape(B, T, H * dh)
```

## Complexity

- **Time:** `O(B·T·D)` — at most one copy of the tensor.
- **Space:** `O(B·T·D)` — the merged copy (splitting returns a view).
