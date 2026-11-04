---
topic: "NumPy Basics"
difficulty: Easy
---
# Join Two Arrays - Solution

## Intuition

Joining along an existing axis and joining along a new axis are different operations. `vstack` and `hstack` (or `concatenate`) grow an axis that already exists. `stack` creates a new axis and places the inputs along it.

## Approach

1. `np.vstack((a, b))` puts the rows of `b` below the rows of `a`. This is the same as `np.concatenate((a, b), axis=0)`.
2. `np.hstack((a, b))` puts the columns of `b` to the right of `a`. This is the same as `np.concatenate((a, b), axis=1)`.
3. `np.stack((a, b), axis=2)` adds a new last axis of length 2, so `stacked[i, j] == [a[i, j], b[i, j]]`.

## Code

```python
import numpy as np

def join_arrays(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    vertical = np.vstack((a, b))
    horizontal = np.hstack((a, b))
    stacked = np.stack((a, b), axis=2)
    return vertical, horizontal, stacked
```
