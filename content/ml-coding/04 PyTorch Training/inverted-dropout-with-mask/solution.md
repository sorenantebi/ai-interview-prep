---
topic: "PyTorch Training"
difficulty: Easy
---
# Inverted Dropout with a Mask - Solution

## Intuition

Each activation survives with probability `1 - p`. Scaling the survivors by `1 / (1 - p)` makes the expected output `(1 - p) · x / (1 - p) = x`, so the network sees the same average signal in training and at inference, where dropout does nothing.

## Approach

1. Multiply `x` by `mask` to zero the dropped activations.
2. Divide by `1 - p` to rescale the survivors.

## Code

```python
import torch

def dropout(x: torch.Tensor, mask: torch.Tensor, p: float) -> torch.Tensor:
    return x * mask / (1 - p)
```

## Complexity

- **Time:** `O(N)` — for `N` elements.
- **Space:** `O(N)` — the output.
