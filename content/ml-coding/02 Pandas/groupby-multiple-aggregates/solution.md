---
topic: "Pandas"
difficulty: Medium
---
# Group By with Several Aggregates - Solution

## Intuition

Named aggregation (`agg(new_name=(column, function))`) computes several statistics in one grouped pass and names the output columns directly.

## Approach

1. Group by `team` (groups come out sorted by key).
2. Aggregate with `players=("player", "nunique")`, `total=("points", "sum")`, `mean=("points", "mean")`, `best=("points", "max")`.
3. `reset_index()` turns `team` back into a column.

## Code

```python
import pandas as pd

def team_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("team")
        .agg(players=("player", "nunique"), total=("points", "sum"), mean=("points", "mean"), best=("points", "max"))
        .reset_index()
    )
```

## Complexity

- **Time:** `O(n log n)` — grouping sorts the team keys.
- **Space:** `O(n)` — the group index.
