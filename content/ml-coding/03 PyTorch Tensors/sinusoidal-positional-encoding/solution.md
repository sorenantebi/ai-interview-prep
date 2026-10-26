---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Sinusoidal Positional Encoding - Solution

## Intuition

The angle is an outer product: positions (a column) times one frequency per pair (a row). Compute the sine and cosine of that `(seq_len, d_model/2)` grid and interleave them into the even and odd columns.

## Approach

1. `pos = arange(seq_len)` as a column; `freq = 10000 ** (-arange(0, d_model, 2) / d_model)` as a row.
2. `angle = pos * freq` by broadcasting.
3. Write `sin(angle)` into `pe[:, 0::2]` and `cos(angle)` into `pe[:, 1::2]`. Computing in float64 and casting at the end keeps large positions accurate.

## Code

```python
import torch

def positional_encoding(seq_len: int, d_model: int) -> torch.Tensor:
    pos = torch.arange(seq_len, dtype=torch.float64).unsqueeze(1)
    freq = 10000.0 ** (-torch.arange(0, d_model, 2, dtype=torch.float64) / d_model)
    angle = pos * freq
    pe = torch.zeros(seq_len, d_model, dtype=torch.float64)
    pe[:, 0::2] = torch.sin(angle)
    pe[:, 1::2] = torch.cos(angle)
    return pe.float()
```

## Complexity

- **Time:** `O(seq_len·d_model)` — one sine or cosine per entry.
- **Space:** `O(seq_len·d_model)` — the encoding.
