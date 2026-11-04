---
topic: "NumPy Basics"
difficulty: Easy
---
# Reverse, Stride and Crop - Solution

## Intuition

NumPy slices accept `start:stop:step` on every axis. A step of `-1` walks backwards and a step of `2` skips every other element, so both requested arrays are single slicing expressions.

## Approach

1. Reverse the rows and take every other column with `a[::-1, ::2]`.
2. Crop the block with `a[r0:r1, c0:c1]`.
3. Return both as a tuple.

## Code

```python
import numpy as np

def slice_views(a: np.ndarray, r0: int, r1: int, c0: int, c1: int) -> tuple[np.ndarray, np.ndarray]:
    return a[::-1, ::2], a[r0:r1, c0:c1]
```

## Complexity

Both results are views, so no data is copied: O(1) extra memory and time.
