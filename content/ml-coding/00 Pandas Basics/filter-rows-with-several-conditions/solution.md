---
topic: "Pandas Basics"
difficulty: Easy
---
# Filter Rows with Several Conditions - Solution

## Intuition

Build one boolean mask from simple pieces: `isin` for the list membership, a comparison for the level, and the boolean column itself. Combine them element-wise with `&` and `|`, then index the DataFrame with the mask.

## Approach

1. Build `df["type"].isin(types)`, a boolean Series.
2. Build `(df["level"] > k) | df["featured"]` for the second condition.
3. Combine the two with `&`. Parentheses are required because `&` and `|` bind tighter than comparisons.
4. Select the rows with `df[mask]` and call `reset_index(drop=True)` for a fresh index.

## Code

```python
import numpy as np
import pandas as pd

def filter_rows(df: pd.DataFrame, types: list[str], k: int) -> pd.DataFrame:
    mask = df["type"].isin(types) & ((df["level"] > k) | df["featured"])
    return df[mask].reset_index(drop=True)
```

## Complexity

Time and memory are both O(n) in the number of rows, since each condition is one vectorised pass over a column.
