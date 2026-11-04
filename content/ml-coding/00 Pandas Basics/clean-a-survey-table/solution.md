---
topic: "Pandas Basics"
difficulty: Easy
---
# Clean a Survey Table - Solution

## Intuition

`fillna` accepts a dict that maps column names to fill values, and `replace` accepts a nested dict that maps column names to `{old: new}` mappings. Each call touches only the columns it names, and each returns a new DataFrame, so chaining them gives the cleaned copy.

## Approach

1. Call `df.fillna(defaults)` to fill the missing values per column.
2. Call `.replace(fixes)` on the result to correct the labels per column.

## Code

```python
import pandas as pd

def clean_table(df: pd.DataFrame, defaults: dict, fixes: dict) -> pd.DataFrame:
    return df.fillna(defaults).replace(fixes)
```

## Complexity

Both calls are a single pass over the affected columns: O(n · c) for n rows and c columns touched.
