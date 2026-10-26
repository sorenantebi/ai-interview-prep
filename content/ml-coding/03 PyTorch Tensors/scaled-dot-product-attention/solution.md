---
topic: "PyTorch Tensors"
difficulty: Hard
---
# Scaled Dot-Product Attention - Solution

## Intuition

Masked keys should vanish from the softmax, which is what a score of `-inf` does (`exp(-inf) = 0`). `torch.softmax` subtracts the row maximum internally, so large scores don't overflow. The only trouble is a row where every key is masked: all scores are `-inf`, the softmax divides 0 by 0 and gives `nan`, so those weights are set to 0.

## Approach

1. `scores = q @ k.transpose(-2, -1) / sqrt(d)` has shape `(B, Tq, Tk)`.
2. If there is a mask, `masked_fill(~mask, -inf)`.
3. Softmax over the last dim, replace `nan` (fully masked rows) with 0, and multiply by `v`.

## Code

```python
import math
import torch

def attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if mask is not None:
        scores = scores.masked_fill(~mask, float("-inf"))
    weights = torch.nan_to_num(torch.softmax(scores, dim=-1), nan=0.0)
    return weights @ v
```

## Complexity

- **Time:** `O(B·Tq·Tk·(d + dv))` — two batched matrix multiplies.
- **Space:** `O(B·Tq·Tk)` — the score and weight matrices.
