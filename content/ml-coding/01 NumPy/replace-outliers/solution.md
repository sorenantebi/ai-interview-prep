---
topic: "NumPy"
difficulty: Medium
---
# Replace Outliers - Solution

## Intuition

Each statistic is a column reduction over `axis=0` with shape `(d,)`, which broadcasts against `x`. A boolean mask marks the outliers and `np.where` picks the median there and the original value elsewhere.

## Approach

1. Compute `mean`, `std` (population) and `median` with `axis=0`.
2. Build the mask `np.abs(x - mean) > 3 * std`.
3. Return `np.where(mask, median, x)`, which creates a new array and leaves `x` unchanged.

## Code

```python
import numpy as np

def replace_outliers(x: np.ndarray) -> np.ndarray:
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    median = np.median(x, axis=0)
    mask = np.abs(x - mean) > 3 * std
    return np.where(mask, median, x).astype(float)
```

## Complexity

- **Time:** `O(n·d log n)`
- **Space:** `O(n·d)`
