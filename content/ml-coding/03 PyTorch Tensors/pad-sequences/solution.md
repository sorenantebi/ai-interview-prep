---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Pad Sequences - Solution

## Intuition

A boolean mask `arange(L) < lengths[:, None]` marks exactly the real-token slots, in row-major order. Assigning the concatenation of all sequences through that mask fills every row at once.

## Approach

1. `lengths = tensor([len(s) for s in seqs])`.
2. Make `padded` of shape `(N, max length)` filled with `pad_value`.
3. Build the mask `arange(L)[None, :] < lengths[:, None]` and assign the flattened tokens through it.

## Code

```python
import torch

def pad_sequences(seqs: list, pad_value: int) -> list:
    lengths = torch.tensor([len(s) for s in seqs], dtype=torch.long)
    padded = torch.full((len(seqs), int(lengths.max())), pad_value, dtype=torch.long)
    mask = torch.arange(padded.shape[1]) < lengths.unsqueeze(1)
    padded[mask] = torch.tensor([v for s in seqs for v in s], dtype=torch.long)
    return [padded, lengths]
```

## Complexity

- **Time:** `O(N·L)` — the padded tensor is written once.
- **Space:** `O(N·L)` — the padded tensor and the mask.
