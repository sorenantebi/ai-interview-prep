---
topic: "Pandas"
difficulty: Medium
---
# Pivot a Sales Table - Solution

## Intuition

This is exactly what `pivot_table` does: it groups by the index and column keys, aggregates, and spreads one key across the columns. `fill_value=0` fills the combinations that never occurred.

## Approach

1. `pivot_table(index="region", columns="month", values="amount", aggfunc="sum", fill_value=0)` (sorted rows and columns).
2. Drop the columns' axis name so the header is just the month strings.
3. `reset_index()` turns `region` back into the first column.

## Code

```python
import pandas as pd

def pivot_sales(df: pd.DataFrame) -> pd.DataFrame:
    table = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", fill_value=0)
    table.columns.name = None
    return table.reset_index()
```

## Complexity

- **Time:** `O(n log n)` — grouping sorts the keys.
- **Space:** `O(r·m)` — the `r` regions by `m` months table.
