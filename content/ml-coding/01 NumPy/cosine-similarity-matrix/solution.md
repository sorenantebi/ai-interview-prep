---
topic: "NumPy"
difficulty: Medium
---
# Cosine Similarity Matrix - Solution

## Intuition

Cosine similarity is the dot product of unit vectors. Normalise every row once, then a single matrix product gives all `n·m` similarities. A zero row stays zero if you divide it by `1` instead of `0`, which gives the required `0.0`.

## Approach

1. Compute row norms by hand: `np.sqrt((a * a).sum(axis=1, keepdims=True))`.
2. Replace zero norms with `1` and divide each array by its norms.
3. Return `a_unit @ b_unit.T`.

## Code

```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    na = np.sqrt((a * a).sum(axis=1, keepdims=True))
    nb = np.sqrt((b * b).sum(axis=1, keepdims=True))
    au = a / np.where(na == 0, 1.0, na)
    bu = b / np.where(nb == 0, 1.0, nb)
    return au @ bu.T
```

## Complexity

- **Time:** `O(n·m·d)`
- **Space:** `O(n·d + m·d + n·m)`
