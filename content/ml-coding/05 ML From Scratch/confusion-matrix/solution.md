---
topic: "ML From Scratch"
difficulty: Easy
---
# Confusion Matrix - Solution

## Intuition

Every sample adds one to exactly one cell, `(true, predicted)`. So the matrix is a 2-D histogram of the label pairs.

## Approach

1. Start from a `num_classes × num_classes` integer array of zeros.
2. Add 1 at every `(y_true[i], y_pred[i])` pair. `np.add.at` does this unbuffered, so repeated pairs are all counted (plain fancy-index `+= 1` would count a repeated pair only once).

## Code

```python
import numpy as np

def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int) -> np.ndarray:
    cm = np.zeros((num_classes, num_classes), dtype=int)
    np.add.at(cm, (y_true, y_pred), 1)
    return cm
```

## Complexity

- **Time:** `O(n + c^2)` — one pass over the samples, plus allocating the matrix for c classes.
- **Space:** `O(c^2)` — the matrix itself.
