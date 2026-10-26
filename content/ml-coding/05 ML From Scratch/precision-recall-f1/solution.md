---
topic: "ML From Scratch"
difficulty: Easy
---
# Precision, Recall and F1 - Solution

## Intuition

Everything comes from three counts: true positives, false positives and false negatives. Count them with boolean masks, then guard each division.

## Approach

1. `tp = sum(pred == 1 and true == 1)`, `fp = sum(pred == 1 and true == 0)`, `fn = sum(pred == 0 and true == 1)`.
2. Precision and recall are the ratios, or `0.0` when their denominator is 0.
3. F1 is their harmonic mean, or `0.0` when both are 0.

## Code

```python
import numpy as np

def precision_recall_f1(y_true: np.ndarray, y_pred: np.ndarray) -> list:
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return [precision, recall, f1]
```

## Complexity

- **Time:** `O(n)` — a few vectorised passes over the labels.
- **Space:** `O(n)` — the temporary boolean masks.
