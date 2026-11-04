---
topic: "Pandas Basics"
difficulty: Easy
---
# Order Totals - Solution

## Intuition

A DataFrame is a dict of columns, so `pd.DataFrame(data)` gives the table directly. Arithmetic between two columns is element-wise, so `price * quantity` computes every row's total at once, and assigning it to a new column name appends it at the end.

## Approach

1. Build `df = pd.DataFrame(data)`.
2. Assign `df["total"] = df["price"] * df["quantity"]`.
3. Return `df`.

## Code

```python
import pandas as pd

def add_total(data: dict[str, list]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["total"] = df["price"] * df["quantity"]
    return df
```

## Complexity

O(n) time and memory. The multiplication is vectorised, so there is no Python-level loop over the rows. `NaN` propagates automatically.
