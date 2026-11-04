---
topic: "Pandas Basics"
difficulty: Easy
---
# Fix the Column Types - Solution

## Intuition

Each column needs one standard conversion: `pd.to_numeric` for numeric strings, `map` with a dict for a fixed set of labels, and `astype` for a plain dtype change. `DataFrame.assign` applies all three and returns a new frame, so the input stays untouched.

## Approach

1. `pd.to_numeric(df["price"], errors="coerce")` parses the strings and turns unparseable ones into `NaN`.
2. `df["member"].map({"yes": True, "no": False})` replaces each label with a bool.
3. `df["count"].astype(float)` changes the int column to float.
4. `df.assign(...)` replaces the three columns on a copy and keeps order and index.

## Code

```python
import pandas as pd

def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        price=pd.to_numeric(df["price"], errors="coerce"),
        member=df["member"].map({"yes": True, "no": False}),
        count=df["count"].astype(float),
    )
```
