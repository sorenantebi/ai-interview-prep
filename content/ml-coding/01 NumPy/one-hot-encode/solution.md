---
topic: "NumPy"
difficulty: Easy
---
# One-Hot Encode - Solution

## Intuition

Each output row has exactly one non-zero entry, at column `labels[i]`. NumPy's integer-array ("fancy") indexing can set all of those entries in a single assignment.

## Approach

1. Allocate an `(n, num_classes)` array of zeros with an integer dtype.
2. Pair every row index `np.arange(n)` with its label and assign `1` at those positions in one indexed assignment.

## Code

```python
import numpy as np

def one_hot(labels: np.ndarray, num_classes: int) -> np.ndarray:
    out = np.zeros((len(labels), num_classes), dtype=int)
    out[np.arange(len(labels)), labels] = 1
    return out
```

## Complexity

- **Time:** `O(n·c)`
- **Space:** `O(n·c)`
