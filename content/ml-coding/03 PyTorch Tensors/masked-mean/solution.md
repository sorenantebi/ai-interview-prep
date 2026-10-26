---
topic: "PyTorch Tensors"
difficulty: Easy
---
# Masked Mean - Solution

## Intuition

Multiplying by the mask zeroes the padding, so a plain sum over time only adds real tokens. Dividing by the number of real tokens gives the mean; clamping that count to at least 1 turns the empty case into 0 / 1 = 0 instead of 0 / 0.

## Approach

1. Cast the mask to `x`'s dtype and add a trailing axis: shape `(B, T, 1)` broadcasts over `D`.
2. Sum `x * m` over dim 1 to get `(B, D)` totals.
3. Sum `m` over dim 1 for the counts, clamp to at least 1, and divide.

## Code

```python
import torch

def masked_mean(x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    m = mask.to(x.dtype).unsqueeze(-1)
    total = (x * m).sum(dim=1)
    count = m.sum(dim=1).clamp(min=1)
    return total / count
```

## Complexity

- **Time:** `O(B·T·D)` — one masked multiply and one sum.
- **Space:** `O(B·T·D)` — the masked copy `x * m`.
