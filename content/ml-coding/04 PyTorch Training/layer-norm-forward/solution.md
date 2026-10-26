---
topic: "PyTorch Training"
difficulty: Medium
---
# Layer Norm Forward - Solution

## Intuition

Each row is shifted to mean 0 and scaled to variance 1 on its own, independent of the rest of the batch. Reducing over the last dimension with `keepdim=True` keeps the per-row statistics broadcastable against the row.

## Approach

1. `mean = x.mean(dim=-1, keepdim=True)`.
2. `var = x.var(dim=-1, unbiased=False, keepdim=True)` (biased: divide by `d`).
3. Normalise with `(x - mean) / torch.sqrt(var + eps)`.
4. Scale by `gamma` and shift by `beta`; both broadcast over the rows.

## Code

```python
import torch

def layer_norm(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, eps: float) -> torch.Tensor:
    mean = x.mean(dim=-1, keepdim=True)
    var = x.var(dim=-1, unbiased=False, keepdim=True)
    return (x - mean) / torch.sqrt(var + eps) * gamma + beta
```

## Complexity

- **Time:** `O(n·d)` — a few passes over `x`.
- **Space:** `O(n·d)` — the normalised copy.
