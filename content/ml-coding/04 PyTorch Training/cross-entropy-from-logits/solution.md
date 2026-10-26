---
topic: "PyTorch Training"
difficulty: Medium
---
# Cross-Entropy from Logits - Solution

## Intuition

`-log softmax(z)[t] = logsumexp(z) - z[t]`. Log-sum-exp is stable once you subtract the row maximum before exponentiating (`torch.logsumexp` does exactly that), so the loss never builds an overflowing `exp`.

## Approach

1. Compute `torch.logsumexp(logits, dim=1)`, one value per example.
2. Pick each example's target logit with `logits[torch.arange(n), targets]` (or `gather`).
3. Return the mean of `logsumexp - target_logit`.

## Code

```python
import torch

def cross_entropy(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    lse = torch.logsumexp(logits, dim=1)
    picked = logits[torch.arange(logits.shape[0]), targets]
    return (lse - picked).mean()
```

## Complexity

- **Time:** `O(n·c)` — one pass over the logits.
- **Space:** `O(n·c)` — `logsumexp`'s temporary shifted copy.
