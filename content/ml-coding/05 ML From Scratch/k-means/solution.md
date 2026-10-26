---
topic: "ML From Scratch"
difficulty: Medium
---
# K-Means - Solution

## Intuition

The two steps each lower the total squared distance: assigning moves each point to its closest centroid, and the mean is the point that minimises the squared distance to a group. Broadcasting computes all point-to-centroid distances at once.

## Approach

1. Copy the centroids as floats.
2. Assign: squared distances `((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)` give an `(n, k)` matrix; `argmin` along axis 1 returns the first (smallest-index) minimum, which handles ties.
3. Update: for each cluster with at least one point, set its centroid to the mean of its points.
4. After the last iteration, return `[centroids, labels]`.

## Code

```python
import numpy as np

def k_means(X: np.ndarray, centroids: np.ndarray, iterations: int) -> list:
    C = np.array(centroids, dtype=float)
    labels = np.zeros(X.shape[0], dtype=int)
    for _ in range(iterations):
        d2 = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
        labels = d2.argmin(axis=1)
        for j in range(C.shape[0]):
            members = X[labels == j]
            if len(members):
                C[j] = members.mean(axis=0)
    return [C, labels]
```

## Complexity

- **Time:** `O(iterations·n·k·d)` — the distance matrix dominates each iteration.
- **Space:** `O(n·k·d)` — the broadcast difference array (O(n·k) if you expand the squared distance instead).
