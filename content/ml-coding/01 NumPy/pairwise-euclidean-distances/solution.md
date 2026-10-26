---
topic: "NumPy"
difficulty: Medium
---
# Pairwise Euclidean Distances - Solution

## Intuition

`|a_i - b_j|² = |a_i|² + |b_j|² - 2·a_i·b_j`. The squared norms are vectors and the dot products are one matrix product `a @ b.T`, so the whole `(n, m)` matrix needs no loops and only `O(n·m)` extra memory.

## Approach

1. Compute squared row norms `aa` (shape `(n, 1)`) and `bb` (shape `(1, m)`).
2. Form `aa + bb - 2 * a @ b.T`, which broadcasts to `(n, m)`.
3. Floating-point rounding can make it slightly negative: clip at `0`, then take the square root.

## Code

```python
import numpy as np

def pairwise_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    aa = (a * a).sum(axis=1)[:, None]
    bb = (b * b).sum(axis=1)[None, :]
    sq = aa + bb - 2.0 * (a @ b.T)
    return np.sqrt(np.maximum(sq, 0.0))
```

## Complexity

- **Time:** `O(n·m·d)`
- **Space:** `O(n·m)`
