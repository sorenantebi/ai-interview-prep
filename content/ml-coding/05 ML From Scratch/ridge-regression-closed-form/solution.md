---
topic: "ML From Scratch"
difficulty: Hard
---
# Ridge Regression (Closed Form) - Solution

## Intuition

Setting the gradient to zero gives `(AᵀA + alpha·D) w = Aᵀy`, where `D` is the identity with its top-left entry (the intercept) set to 0. That matrix is positive definite whenever `alpha > 0`, so a plain linear solve works.

## Approach

1. Build `A = [1 | X]`.
2. `D = alpha · I` of size `d + 1`, then set `D[0, 0] = 0` so the intercept isn't penalised.
3. Solve `(AᵀA + D) w = Aᵀy` with `np.linalg.solve` (no explicit inverse).

Equivalently: center `X` and `y`, solve the penalised problem without an intercept, and recover the intercept as `mean(y) - mean(X) · w[1:]`.

## Code

```python
import numpy as np

def ridge_regression(X: np.ndarray, y: np.ndarray, alpha: float) -> np.ndarray:
    A = np.hstack([np.ones((X.shape[0], 1)), X])
    D = alpha * np.eye(A.shape[1])
    D[0, 0] = 0.0
    return np.linalg.solve(A.T @ A + D, A.T @ y)
```

## Complexity

- **Time:** `O(n·d^2 + d^3)` — forming AᵀA and solving the (d+1) × (d+1) system.
- **Space:** `O(n·d + d^2)` — the augmented matrix and AᵀA.
