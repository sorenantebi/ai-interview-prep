---
topic: "ML From Scratch"
difficulty: Medium
---
# Gaussian Naive Bayes - Solution

## Intuition

Naive Bayes treats the features as independent within a class, so the log-likelihood of a point is a sum of 1-D Gaussian log densities. Working in logs avoids multiplying many tiny probabilities.

## Approach

1. `classes = np.unique(y_train)` (sorted).
2. For each class, compute its prior, feature means and variances (`var(axis=0) + eps`).
3. Score all test points against all classes with broadcasting, giving a `(q, n_classes)` matrix.
4. `argmax` along the classes returns the first (smallest label) among ties; map back through `classes`.

## Code

```python
import numpy as np

def gaussian_nb_predict(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, eps: float) -> np.ndarray:
    classes = np.unique(y_train)
    mu = np.array([X_train[y_train == c].mean(axis=0) for c in classes])
    var = np.array([X_train[y_train == c].var(axis=0) for c in classes]) + eps
    log_prior = np.log(np.array([(y_train == c).mean() for c in classes]))
    diff = X_test[:, None, :] - mu[None, :, :]
    log_lik = -0.5 * (np.log(2 * np.pi * var)[None] + diff ** 2 / var[None]).sum(axis=2)
    return classes[(log_prior[None] + log_lik).argmax(axis=1)]
```

## Complexity

- **Time:** `O((m + q)·d·c)` — fitting touches every training value once per class; scoring compares every test point with every class.
- **Space:** `O(q·d·c)` — the broadcast differences (c classes).
