---
topic: "NumPy"
difficulty: Medium
---
# Batched Bilinear Scores - Solution

## Intuition

For one batch element the scores are `q[b] @ w @ keys[b].T`. NumPy's `@` treats every axis except the last two as a batch axis (and broadcasts the shared 2-D `w` across it), so the same expression works for the whole batch once the keys are transposed on their last two axes.

## Approach

1. Transform the queries once: `qw = q @ w`, shape `(B, n, d)`.
2. Transpose the keys to `(B, d, m)` with `keys.transpose(0, 2, 1)` (or `np.swapaxes(keys, 1, 2)`).
3. Batched matrix product: `qw @ keys_t`, shape `(B, n, m)`.

## Code

```python
import numpy as np

def bilinear_scores(q: np.ndarray, w: np.ndarray, keys: np.ndarray) -> np.ndarray:
    return (q @ w) @ keys.transpose(0, 2, 1)
```

## Complexity

- **Time:** `O(B·n·d·(d + m))`
- **Space:** `O(B·n·(d + m))`
