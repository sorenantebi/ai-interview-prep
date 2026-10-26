---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Gather Target Probabilities - Solution

## Intuition

`torch.gather` picks one element per position along a dimension, using an index tensor of the same rank. Giving the targets a trailing size-1 axis makes them that index along the class dimension.

## Approach

1. `targets.unsqueeze(-1)` has shape `(..., 1)`.
2. `probs.gather(-1, ...)` returns `(..., 1)` with the chosen probabilities.
3. `.squeeze(-1)` drops the extra axis.

## Code

```python
import torch

def gather_target_probs(probs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    return probs.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
```

## Complexity

- **Time:** `O(N)` — for `N` target positions, one lookup each.
- **Space:** `O(N)` — the output.
