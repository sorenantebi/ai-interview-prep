---
topic: "Pandas"
difficulty: Easy
---
# Top N Value Counts - Solution

## Intuition

`value_counts` does the counting; the only subtlety is a deterministic tie-break, which needs a sort on two keys.

## Approach

1. Count with `s.value_counts()` (drops missing values).
2. Sort by count descending, then by label ascending.
3. Keep the first `n` rows.

## Code

```python
import pandas as pd

def top_values(s: pd.Series, n: int) -> pd.Series:
    counts = s.value_counts()
    table = pd.DataFrame({"label": counts.index, "count": counts.values})
    table = table.sort_values(["count", "label"], ascending=[False, True]).head(n)
    return pd.Series(table["count"].values, index=table["label"].values)
```

## Complexity

- **Time:** `O(n + d log d)` — counting, then sorting the `d` distinct labels.
- **Space:** `O(d)` — one entry per distinct label.
