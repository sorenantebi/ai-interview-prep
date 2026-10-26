---
topic: "NumPy"
difficulty: Easy
---
# Min-Max Scale Columns - Solution

## Intuition

Column minimums and maximums are reductions over `axis=0`; their shape `(d,)` broadcasts against `(n, d)`, so one expression scales every column. Constant columns only need a safe divisor.

## Approach

1. Compute `lo = x.min(axis=0)` and `span = x.max(axis=0) - lo`.
2. Replace zero spans with `1` so constant columns divide `0 / 1 = 0` instead of `0 / 0`.
3. Return `(x - lo) / span`.

## Code

```python
import numpy as np

def min_max_scale(x: np.ndarray) -> np.ndarray:
    lo = x.min(axis=0)
    span = x.max(axis=0) - lo
    span = np.where(span == 0, 1.0, span)
    return (x - lo) / span
```

## Complexity

- **Time:** `O(n·d)`
- **Space:** `O(n·d)`
