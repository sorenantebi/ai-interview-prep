---
topic: "NumPy Basics"
difficulty: Easy
---
# Circle Areas and Circumferences - Solution

## Intuition

NumPy arithmetic is element-wise, so `np.pi * radii ** 2` computes every area in one expression, and `2 * np.pi * radii` computes every circumference. `np.vstack` then stacks the two 1-D results as rows of a `(2, n)` array.

## Approach

1. Compute the areas with `np.pi * radii ** 2`.
2. Compute the circumferences with `2 * np.pi * radii`.
3. Stack them with `np.vstack`, giving shape `(2, n)`.

## Code

```python
import numpy as np

def circle_stats(radii: np.ndarray) -> np.ndarray:
    areas = np.pi * radii ** 2
    circumferences = 2 * np.pi * radii
    return np.vstack([areas, circumferences])
```

## Complexity

Time and memory are both O(n).
