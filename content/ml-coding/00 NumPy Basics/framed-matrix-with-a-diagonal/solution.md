---
topic: "NumPy Basics"
difficulty: Easy
---
# Framed Matrix with a Diagonal - Solution

## Intuition

Start from a matrix of ones, zero out the interior with a slice, then overwrite the diagonal. `np.eye(n, dtype=bool)` gives a boolean mask of the diagonal, so the diagonal can override the border in one assignment.

## Approach

1. Create `np.ones((n, n))`, which makes every cell `1`.
2. Set the interior slice `[1:-1, 1:-1]` to `0`. For `n <= 2` the slice is empty, so nothing changes.
3. Use `np.eye(n, dtype=bool)` as a mask and assign `value` on the diagonal.

## Code

```python
import numpy as np

def framed_matrix(n: int, value: float) -> np.ndarray:
    out = np.ones((n, n))
    out[1:-1, 1:-1] = 0
    out[np.eye(n, dtype=bool)] = value
    return out
```
