---
topic: "NumPy Basics"
difficulty: Easy
---
# Array Attributes - Solution

## Intuition

An `ndarray` already stores everything the task asks for as attributes, so no computation is needed, only knowing the attribute names.

## Approach

1. Read `x.ndim` for the number of dimensions.
2. Read `x.shape`, which is already a tuple of ints.
3. Read `x.size` for the total element count (the product of the shape).
4. Read `x.dtype.name` to get the dtype as a plain string.

## Code

```python
import numpy as np

def array_info(x: np.ndarray) -> tuple[int, tuple[int, ...], int, str]:
    return x.ndim, x.shape, x.size, x.dtype.name
```

## Complexity

All four attributes are stored on the array, so this is O(1) time and does not touch the data.
