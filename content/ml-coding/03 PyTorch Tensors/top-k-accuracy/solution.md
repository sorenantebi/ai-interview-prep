---
topic: "PyTorch Tensors"
difficulty: Hard
---
# Top-k Accuracy - Solution

## Intuition

You don't need to sort at all. A target is in the top `k` exactly when fewer than `k` classes beat it, and counting the classes that beat it is a comparison against the target's own logit, broadcast over the row. That definition also handles ties cleanly.

## Approach

1. Pick each target's logit with `gather`: shape `(N, 1)`.
2. Count the strictly greater logits per row: `(logits > target_logit).sum(1)`.
3. Correct where that count is `< k`; average as a float and return `.item()`.

## Code

```python
import torch

def top_k_accuracy(logits: torch.Tensor, targets: torch.Tensor, k: int) -> float:
    target_logit = logits.gather(1, targets.unsqueeze(1))
    higher = (logits > target_logit).sum(dim=1)
    return (higher < k).float().mean().item()
```

## Complexity

- **Time:** `O(N·C)` — one comparison per logit, no sorting.
- **Space:** `O(N·C)` — the boolean comparison matrix.
