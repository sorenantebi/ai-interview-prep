---
topic: "NumPy Basics"
difficulty: Easy
---
# Range Grid - Solution

## Intuition

`np.arange(start, stop)` gives a flat array of consecutive integers. `reshape` fills a new shape in row-major order, and one dimension may be `-1`, meaning "infer this size from the total number of elements".

## Approach

1. Create the flat array with `np.arange(start, stop)`.
2. Reshape it to `(rows, -1)`; NumPy infers the number of columns as `size // rows`.

## Code

```python
import numpy as np

def range_grid(start: int, stop: int, rows: int) -> np.ndarray:
    return np.arange(start, stop).reshape(rows, -1)
```
