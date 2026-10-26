---
topic: "Pandas"
difficulty: Medium
---
# Left Join and Fill - Solution

## Intuition

A left merge keeps every order exactly once (the customer keys are unique) and preserves the left frame's row order; unmatched orders get `NaN`, which `fillna` replaces.

## Approach

1. `orders.merge(customers, on="customer_id", how="left")`.
2. Fill missing `name` and `country` with `"unknown"`.

## Code

```python
import pandas as pd

def join_orders(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    out = orders.merge(customers, on="customer_id", how="left")
    out[["name", "country"]] = out[["name", "country"]].fillna("unknown")
    return out
```

## Complexity

- **Time:** `O(n + m)` — a hash join of `n` orders against `m` customers.
- **Space:** `O(n + m)` — the hash table and the result.
