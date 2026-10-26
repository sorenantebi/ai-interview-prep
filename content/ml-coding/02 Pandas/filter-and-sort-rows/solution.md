---
topic: "Pandas"
difficulty: Easy
---
# Filter and Sort Rows - Solution

## Intuition

A boolean mask picks the rows; `sort_values` with two keys and a direction per key handles the tie-break.

## Approach

1. Keep the rows where `df["score"] >= min_score`.
2. Sort by `["score", "name"]` with `ascending=[False, True]`.
3. `reset_index(drop=True)` so the index is `0..n-1` again.

## Code

```python
import pandas as pd

def filter_and_sort(df: pd.DataFrame, min_score: float) -> pd.DataFrame:
    kept = df[df["score"] >= min_score]
    return kept.sort_values(["score", "name"], ascending=[False, True]).reset_index(drop=True)
```

## Complexity

- **Time:** `O(n log n)` — the sort.
- **Space:** `O(n)` — the filtered copy.
