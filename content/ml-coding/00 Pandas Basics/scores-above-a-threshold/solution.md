---
topic: "Pandas Basics"
difficulty: Easy
---
# Scores Above a Threshold - Solution

## Intuition

A `pd.Series` built from a dict uses the keys as its index. Comparing a Series with a number gives a boolean Series with the same index, which can be used directly as a mask.

## Approach

1. Build `s = pd.Series(scores)`.
2. Compute the mask `s > threshold`.
3. Select with `s.loc[mask]`, which keeps the labels as the index.

## Code

```python
import pandas as pd

def above_threshold(scores: dict[str, float], threshold: float) -> pd.Series:
    s = pd.Series(scores)
    return s.loc[s > threshold]
```
