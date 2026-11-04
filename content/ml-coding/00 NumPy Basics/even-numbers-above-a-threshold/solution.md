---
topic: "NumPy Basics"
difficulty: Easy
---
# Even Numbers Above a Threshold - Solution

## Intuition

Each condition becomes a boolean mask of the same shape as `x`. Combining the masks with `&` keeps only the positions where both hold, and indexing with the combined mask picks those elements in their original order.

## Approach

1. Build `x % 2 == 0` to mark even elements (this also works correctly for negative numbers, since NumPy's `%` returns a non-negative result for a positive divisor).
2. Build `x > k` to mark elements above the threshold.
3. Combine with `&` (each comparison in parentheses, because `&` binds tighter than `==` and `>`).
4. Return `x[mask]`, which is a new array.

## Code

```python
import numpy as np

def filter_even_above(x: np.ndarray, k: int) -> np.ndarray:
    mask = (x % 2 == 0) & (x > k)
    return x[mask]
```
