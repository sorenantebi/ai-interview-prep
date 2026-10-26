---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Batched Pairwise Distances - Solution

## Intuition

Expand the square: `||x - y||² = ||x||² + ||y||² - 2·x·y`. The cross term for all pairs is one batched matrix multiply, so memory stays `O(B·N·M)` instead of `O(B·N·M·D)`. Rounding can make the squared distance of two equal points a tiny negative number, so clamp at 0 before the square root, or you get `nan`.

## Approach

1. Squared norms: `(a*a).sum(-1, keepdim=True)` is `(B, N, 1)`, `(b*b).sum(-1)` reshaped to `(B, 1, M)`.
2. Cross term: `a @ b.transpose(1, 2)` is `(B, N, M)`.
3. Combine, clamp at 0, take the square root.

## Code

```python
import torch

def pairwise_distances(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    sq = (a * a).sum(-1, keepdim=True) + (b * b).sum(-1).unsqueeze(1) - 2 * a @ b.transpose(1, 2)
    return sq.clamp_min(0).sqrt()
```

## Complexity

- **Time:** `O(B·N·M·D)` — dominated by the batched matrix multiply.
- **Space:** `O(B·N·M)` — the output and the cross-term matrix.
