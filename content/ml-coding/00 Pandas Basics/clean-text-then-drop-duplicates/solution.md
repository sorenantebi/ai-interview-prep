---
topic: "Pandas Basics"
difficulty: Easy
---
# Clean Text, Then Drop Duplicates - Solution

## Intuition

Rows like `" Berlin"` and `"berlin "` only look different because of whitespace and case. If we standardise the text column first, they become equal and `drop_duplicates` can remove them. Doing it in the opposite order would miss those duplicates.

## Approach

1. Use `.str.strip().str.lower()` on the `"city"` column and put the result back with `assign`, which returns a new DataFrame, so the input is not modified.
2. Call `drop_duplicates(keep="first")`, which compares all columns and keeps the first occurrence along with its original index label.

## Code

```python
import pandas as pd

def clean_and_dedupe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.assign(city=df["city"].str.strip().str.lower())
    return df.drop_duplicates(keep="first")
```
