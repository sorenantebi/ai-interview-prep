---
topic: "ML From Scratch"
difficulty: Medium
---
# K-Nearest Neighbours Classifier - Solution

## Intuition

Compute every test-to-train distance in one broadcast, take the `k` smallest per row with a stable sort (so equal distances keep training order), then count votes.

## Approach

1. Squared distances `((X_test[:, None] - X_train[None]) ** 2).sum(-1)`, shape `(q, m)`. Squaring doesn't change the order.
2. `np.argsort(..., kind="stable", axis=1)[:, :k]` gives the neighbour indices; a stable sort keeps the smaller training index first among equal distances.
3. For each test row, `np.bincount` of the neighbour labels counts the votes and `argmax` returns the smallest label among the ties.

## Code

```python
import numpy as np

def knn_classify(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, k: int) -> np.ndarray:
    d2 = ((X_test[:, None, :] - X_train[None, :, :]) ** 2).sum(axis=2)
    nearest = np.argsort(d2, axis=1, kind="stable")[:, :k]
    votes = y_train[nearest]
    return np.array([np.bincount(row).argmax() for row in votes], dtype=int)
```

## Complexity

- **Time:** `O(q·m·(d + log m))` — the distance matrix plus sorting each row.
- **Space:** `O(q·m·d)` — the broadcast difference array.
