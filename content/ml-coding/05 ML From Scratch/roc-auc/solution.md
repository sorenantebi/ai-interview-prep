---
topic: "ML From Scratch"
difficulty: Medium
---
# ROC AUC - Solution

## Intuition

Sort all scores and give them ranks, averaging the ranks of tied scores. The sum of the positives' ranks counts, for each positive, how many scores sit below it (ties count half). Subtracting the positives' own contribution leaves exactly the number of winning (positive, negative) pairs: the Mann–Whitney U statistic.

## Approach

1. Sort the scores and assign ranks 1..n; tied scores all get the average of their ranks.
2. `U = sum(ranks of positives) - P·(P + 1)/2`, where `P` is the number of positives.
3. `AUC = U / (P · N)` with `N` negatives.

## Code

```python
import numpy as np

def roc_auc(y_true: np.ndarray, scores: np.ndarray) -> float:
    order = np.argsort(scores, kind="stable")
    s = scores[order]
    ranks = np.empty(len(s))
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1  # average rank of the tied run
        i = j + 1
    pos = y_true == 1
    P, N = int(pos.sum()), int((~pos).sum())
    U = ranks[pos].sum() - P * (P + 1) / 2
    return float(U / (P * N))
```

## Complexity

- **Time:** `O(n log n)` — sorting the scores; the rank pass is linear.
- **Space:** `O(n)` — the order and rank arrays.
