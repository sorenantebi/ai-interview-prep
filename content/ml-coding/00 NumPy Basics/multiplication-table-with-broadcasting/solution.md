---
topic: "NumPy Basics"
difficulty: Easy
---
# Multiplication Table with Broadcasting - Solution

## Intuition

A column vector of shape `(n, 1)` multiplied by a row vector of shape `(m,)` broadcasts to shape `(n, m)`, and entry `[i, j]` is the product of the `i`-th and `j`-th elements. That is exactly the multiplication table.

## Approach

1. Create `rows = np.arange(1, n + 1)` and `cols = np.arange(1, m + 1)`.
2. Turn `rows` into a column with `rows[:, None]`, shape `(n, 1)`.
3. Multiply: `(n, 1) * (m,)` broadcasts to `(n, m)`.

## Code

```python
import numpy as np

def multiplication_table(n: int, m: int) -> np.ndarray:
    return np.arange(1, n + 1)[:, None] * np.arange(1, m + 1)
```

## Complexity

Time and memory are `O(n * m)`, the size of the output.
