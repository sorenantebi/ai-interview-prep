---
topic: "ML From Scratch"
difficulty: Easy
---
# Linear Regression (Normal Equation) - Solution

## Intuition

Setting the gradient of the squared error to zero gives the normal equation `AᵀA w = Aᵀy`. A least-squares solver solves it stably and also handles the singular case by returning the minimum-norm solution.

## Approach

1. Build `A = [1 | X]` by prepending a column of ones.
2. Solve the least-squares problem `A w ≈ y` with `np.linalg.lstsq(A, y, rcond=None)`, which returns the minimum-norm solution when `AᵀA` is singular.

## Code

```python
import numpy as np

def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    A = np.hstack([np.ones((X.shape[0], 1)), X])
    w, *_ = np.linalg.lstsq(A, y, rcond=None)
    return w
```

## Complexity

- **Time:** `O(n·d^2)` — the least-squares solve (SVD-based) on an n × (d+1) matrix.
- **Space:** `O(n·d)` — the augmented design matrix.
