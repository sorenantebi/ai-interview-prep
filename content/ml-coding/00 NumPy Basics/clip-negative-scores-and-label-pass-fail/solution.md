---
topic: "NumPy Basics"
difficulty: Easy
---
# Clip Negative Scores and Label Pass/Fail - Solution

## Intuition

`np.where(condition, a, b)` picks elementwise from `a` where the condition is true and from `b` otherwise. Use it once to zero out negatives and once more to turn a boolean comparison into string labels.

## Approach

1. `clean = np.where(scores < 0, 0.0, scores)` replaces negatives with 0.
2. `labels = np.where(clean >= threshold, 'pass', 'fail')` produces a string array from the cleaned scores.
3. Return `clean` and `labels.tolist()` so the labels are a plain Python list.

## Code

```python
import numpy as np

def clean_and_label(scores: np.ndarray, threshold: float) -> tuple[np.ndarray, list[str]]:
    clean = np.where(scores < 0, 0.0, scores)
    return clean, np.where(clean >= threshold, 'pass', 'fail').tolist()
```
