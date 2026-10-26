---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Scatter-Add Counts - Solution

## Intuition

`index_add_` adds row `i` of a source into row `labels[i]` of a destination in one vectorized call, which is exactly a per-class sum. `bincount` gives the per-class counts. Dividing by the counts, clamped to at least 1, gives the means and leaves empty classes at 0.

## Approach

1. Start from zeros of shape `(num_classes, D)` and `index_add_(0, labels, x)` to get the sums.
2. `torch.bincount(labels, minlength=num_classes)` gives the counts.
3. Divide the sums by `counts.clamp(min=1)` with a trailing axis so it broadcasts over `D`.

## Code

```python
import torch

def class_means(x: torch.Tensor, labels: torch.Tensor, num_classes: int) -> torch.Tensor:
    sums = torch.zeros(num_classes, x.shape[1], dtype=x.dtype).index_add_(0, labels, x)
    counts = torch.bincount(labels, minlength=num_classes).to(x.dtype)
    return sums / counts.clamp(min=1).unsqueeze(1)
```

## Complexity

- **Time:** `O(N·D + num_classes·D)` — one pass to scatter the rows, one to divide.
- **Space:** `O(num_classes·D)` — the sums (the output).
