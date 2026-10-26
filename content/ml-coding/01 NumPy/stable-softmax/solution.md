---
topic: "NumPy"
difficulty: Easy
---
# Stable Softmax - Solution

## Intuition

Softmax doesn't change if you subtract the same constant from every score in a row, because the factor `exp(-c)` cancels between numerator and denominator. Subtracting the row maximum makes the largest exponent `exp(0) = 1`, so nothing overflows.

## Approach

1. Take the maximum of each row with `keepdims=True` so it broadcasts against `x`.
2. Exponentiate `x - max`.
3. Divide by the row sums (again with `keepdims=True`).

## Code

```python
import numpy as np

def softmax(x: np.ndarray) -> np.ndarray:
    z = x - x.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)
```

## Complexity

- **Time:** `O(n·k)` — a constant number of passes over the array.
- **Space:** `O(n·k)` — the shifted and exponentiated copies.
