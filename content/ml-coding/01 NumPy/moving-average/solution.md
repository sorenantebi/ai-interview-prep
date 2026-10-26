---
topic: "NumPy"
difficulty: Easy
---
# Moving Average - Solution

## Intuition

The sum of `x[i : i + k]` is the difference of two prefix sums. With a prefix-sum array that starts at `0`, all `n - k + 1` window sums come from one vectorised subtraction.

## Approach

1. Build `c = [0, x[0], x[0] + x[1], …]` with `np.cumsum` and a leading zero.
2. Window sums are `c[k:] - c[:-k]`; divide by `k`.

## Code

```python
import numpy as np

def moving_average(x: np.ndarray, k: int) -> np.ndarray:
    c = np.concatenate([[0.0], np.cumsum(x, dtype=float)])
    return (c[k:] - c[:-k]) / k
```

## Complexity

- **Time:** `O(n)`
- **Space:** `O(n)`
