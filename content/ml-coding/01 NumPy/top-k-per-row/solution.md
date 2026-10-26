---
topic: "NumPy"
difficulty: Medium
---
# Top-K per Row - Solution

## Intuition

Sorting each row by descending value gives the answer in its first `k` columns. Sorting `-x` ascending with a stable sort keeps equal values in index order, which is exactly the required tie-break.

## Approach

1. `np.argsort(-x, axis=1, kind="stable")` sorts every row's indices by descending value, ties by index.
2. Keep the first `k` columns.
3. (For large `d`, `np.argpartition` then sorting only the `k` candidates is faster, but ties need extra care.)

## Code

```python
import numpy as np

def top_k_per_row(x: np.ndarray, k: int) -> np.ndarray:
    return np.argsort(-x, axis=1, kind="stable")[:, :k]
```

## Complexity

- **Time:** `O(n·d log d)`
- **Space:** `O(n·d)`
