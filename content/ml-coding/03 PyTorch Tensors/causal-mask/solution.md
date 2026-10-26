---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Causal Mask - Solution

## Intuition

The forbidden entries are exactly those strictly above the main diagonal, which is what `triu(1)` keeps.

## Approach

1. Fill a `(t, t)` float32 tensor with `-inf`.
2. `.triu(1)` keeps the entries above the diagonal and sets the diagonal and everything below it to 0.

## Code

```python
import torch

def causal_mask(t: int) -> torch.Tensor:
    return torch.full((t, t), float("-inf")).triu(1)
```

## Complexity

- **Time:** `O(t²)` — every entry is written once.
- **Space:** `O(t²)` — the mask itself.
