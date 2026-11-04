---
topic: "Pandas Basics"
difficulty: Easy
---
# First Rows, Last Two Columns - Solution

## Intuition

`.iloc` selects by integer position and takes a row selector and a column selector separated by a comma. A slice `:n` gives the first `n` rows, and the negative slice `-2:` gives the last two columns, whatever the frame's width. Since `.iloc` keeps the index and the column labels, nothing else is needed.

## Approach

1. Use `df.iloc[:n, -2:]`: rows `0..n-1`, columns from the second-to-last to the end.
2. Return the result.

## Code

```python
import numpy as np
import pandas as pd

def top_left_slice(df: pd.DataFrame, n: int) -> pd.DataFrame:
    return df.iloc[:n, -2:]
```
