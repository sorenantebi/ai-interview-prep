---
topic: "ML From Scratch"
difficulty: Hard
---
# Decision Stump: Best Gini Split - Solution

## Intuition

Sort each feature once. Moving the threshold past one more distinct value moves a group of samples from the right side to the left, so cumulative class counts along the sorted order give the left and right label counts for every candidate at once.

## Approach

1. One-hot encode `y` (shape `(n, C)`).
2. For each feature, sort the samples by that feature and take cumulative sums of the one-hot rows: row `i` holds the class counts of the first `i + 1` samples, i.e. the left side when the threshold falls just after sample `i`.
3. Valid cut positions are where the sorted value changes (`v[i] < v[i + 1]`); the threshold there is `(v[i] + v[i + 1]) / 2`.
4. Compute both Gini impurities and the weighted score for every valid cut.
5. Scan features in order and thresholds in increasing order, replacing the best only when a score is lower by more than `1e-12`, which implements the tie-breaking rule.

## Code

```python
import numpy as np

def best_split(X: np.ndarray, y: np.ndarray) -> list:
    n, d = X.shape
    onehot = (y[:, None] == np.unique(y)[None, :]).astype(float)
    total = onehot.sum(axis=0)

    def gini(counts, size):
        return 1.0 - ((counts / size[:, None]) ** 2).sum(axis=1)

    best = [-1, 0.0, float(1.0 - ((total / n) ** 2).sum())]
    best_score = np.inf
    for f in range(d):
        order = np.argsort(X[:, f], kind="stable")
        v = X[order, f]
        cuts = np.nonzero(v[:-1] < v[1:])[0]
        if len(cuts) == 0:
            continue
        left = np.cumsum(onehot[order], axis=0)[cuts]
        n_left = (cuts + 1).astype(float)
        n_right = n - n_left
        scores = (n_left * gini(left, n_left) + n_right * gini(total - left, n_right)) / n
        thresholds = (v[cuts] + v[cuts + 1]) / 2
        for s, t in zip(scores, thresholds):
            if s < best_score - 1e-12:
                best_score, best = s, [f, float(t), float(s)]
    return best
```

## Complexity

- **Time:** `O(d·n·(log n + C))` — sorting each feature plus cumulative counts over C classes.
- **Space:** `O(n·C)` — the one-hot labels and cumulative counts.
