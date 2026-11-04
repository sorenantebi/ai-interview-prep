---
topic: "NumPy Basics"
difficulty: Easy
---
# Celsius to Fahrenheit - Solution

## Intuition

NumPy arithmetic operators work element-wise on whole arrays, so the conversion formula can be written exactly as for a single number. `np.round` then rounds every element at once.

## Approach

1. Compute `celsius * 9 / 5 + 32`. The result is a new float array, so the input is untouched.
2. Pass it to `np.round(..., 1)` to round each element to 1 decimal.

## Code

```python
import numpy as np

def celsius_to_fahrenheit(celsius: np.ndarray) -> np.ndarray:
    return np.round(celsius * 9 / 5 + 32, 1)
```

## Complexity

Time and extra memory are both O(n) in the number of elements, with no Python-level loop.
