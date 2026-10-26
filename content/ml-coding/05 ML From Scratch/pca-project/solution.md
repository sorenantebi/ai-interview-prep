---
topic: "ML From Scratch"
difficulty: Medium
---
# PCA Projection - Solution

## Intuition

The singular value decomposition of the centered data `Xc = U S Vᵀ` gives the covariance eigenvectors as the rows of `Vᵀ`, already sorted by decreasing variance (`S² / (n - 1)`). Projecting is then a matrix product. Only the sign needs fixing.

## Approach

1. `Xc = X - X.mean(axis=0)`.
2. `_, _, Vt = np.linalg.svd(Xc, full_matrices=False)`; the first `k` rows of `Vt` are the components.
3. For each component, find the index of its largest absolute entry (`argmax` returns the first) and multiply the component by -1 if that entry is negative.
4. Return `Xc @ components.T`.

## Code

```python
import numpy as np

def pca_project(X: np.ndarray, k: int) -> np.ndarray:
    Xc = X - X.mean(axis=0)
    _, _, Vt = np.linalg.svd(Xc, full_matrices=False)
    comps = Vt[:k]
    signs = np.sign(comps[np.arange(k), np.abs(comps).argmax(axis=1)])
    comps = comps * signs[:, None]
    return Xc @ comps.T
```

## Complexity

- **Time:** `O(n·d^2)` — the thin SVD of an n × d matrix (n ≥ d).
- **Space:** `O(n·d)` — the centered copy and the SVD factors.
