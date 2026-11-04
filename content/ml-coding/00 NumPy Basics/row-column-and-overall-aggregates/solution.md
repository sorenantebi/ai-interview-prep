---
topic: "NumPy Basics"
difficulty: Easy
---
# Row, Column and Overall Aggregates - Solution

## Intuition

Every NumPy reduction takes an `axis` argument: the axis you name is the one that gets collapsed. `axis=1` collapses the columns of each row (one result per row), `axis=0` collapses the rows of each column (one result per column), and no axis collapses everything.

## Approach

1. `x.sum(axis=1)` gives one sum per row, shape `(n,)`.
2. `x.mean(axis=0)` gives one mean per column, shape `(d,)`.
3. `x.max()` gives the largest entry overall.
4. `x.argmax(axis=0)` gives the row index of each column's maximum; on ties NumPy returns the first index.

## Code

```python
import numpy as np

def aggregate_stats(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, np.ndarray]:
    return x.sum(axis=1), x.mean(axis=0), x.max(), x.argmax(axis=0)
```
