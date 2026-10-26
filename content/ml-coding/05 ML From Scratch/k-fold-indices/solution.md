---
topic: "ML From Scratch"
difficulty: Easy
---
# K-Fold Indices - Solution

## Intuition

Once you know where each fold starts and ends, each validation set is a slice of `range(n)` and the training set is everything else.

## Approach

1. Fold sizes are `n // k + 1` for the first `n % k` folds and `n // k` for the rest.
2. Walk through the sizes keeping a running start; fold `i` validates on `[start, start + size)`.
3. The training indices are the indices before the block followed by those after it.

## Code

```python
import numpy as np

def k_fold_indices(n: int, k: int) -> list:
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    folds, start = [], 0
    for size in sizes:
        val = list(range(start, start + size))
        train = list(range(0, start)) + list(range(start + size, n))
        folds.append([train, val])
        start += size
    return folds
```

## Complexity

- **Time:** `O(n·k)` — each of the k folds lists all n indices.
- **Space:** `O(n·k)` — the returned lists.
