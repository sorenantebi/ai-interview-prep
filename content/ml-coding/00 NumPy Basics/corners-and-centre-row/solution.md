---
topic: "NumPy Basics"
difficulty: Easy
---
# Corners and Centre Row - Solution

## Intuition

Negative indices count from the end, so `0` and `-1` address the first and last row or column without needing `n` or `m`. The centre row is a plain row lookup `a[i]` with `i = n // 2`.

## Approach

1. Read the four corners with `a[0, 0]`, `a[0, -1]`, `a[-1, 0]`, `a[-1, -1]` and put them in a length-4 array.
2. Take the centre row with `a[a.shape[0] // 2]`.
3. Return both as a tuple.

## Code

```python
import numpy as np

def corners_and_centre(a: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    corners = np.array([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]])
    return corners, a[a.shape[0] // 2]
```
