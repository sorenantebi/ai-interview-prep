# Learn: Decision Stump: Best Gini Split

## The idea

- **Decision stump**: a decision tree with just one yes/no question, like "is feature 0 at most 2.5?".
- The task: find the best feature and threshold for that one question, the one a tree would pick at its root.
- Tree libraries run this same search at every node while training, so it is the core step of tree building.
- **Gini impurity**: a number for how mixed a group of labels is.
  - All labels the same (a pure group) gives 0.
  - Two classes split 50/50 gives 0.5.
  - Formula: `1 - Σ p_c²`, where `p_c` is the fraction of labels in class `c`.
- **Split**: a feature `f` and a **threshold** `t`; samples with `X[i, f] <= t` go left, the rest go right.
- **Score**: the Gini of the left and right groups, averaged and weighted by group size. Lower is better.
- **Candidate thresholds**: midpoints between consecutive distinct sorted values of a feature.
- **Cumulative counts**: moving the cut one step right just moves one sample from right to left, so counts change by one. No need to recount from scratch.
- **One-hot encoding**: turning each label into a row of 0s with a single 1, so that summing rows gives class counts.
- **Broadcasting**: NumPy stretches a smaller array to match a bigger one in arithmetic, e.g. a `(k, 1)` column against a `(k, C)` table.

## Work it by hand

Example 1: `X = [[1], [2], [3], [4]]`, `y = [0, 0, 1, 1]`, so `n = 4` and one feature.

1. Sorted values: `1, 2, 3, 4`. Candidates: `1.5`, `2.5`, `3.5`.
2. Score each candidate:

| threshold | left labels | right labels | Gini left | Gini right | score |
|---|---|---|---|---|---|
| 1.5 | [0] | [0, 1, 1] | 0 | 1 - (1/9 + 4/9) = 0.4444 | 3/4 · 0.4444 = 0.3333 |
| 2.5 | [0, 0] | [1, 1] | 0 | 0 | 0 |
| 3.5 | [0, 0, 1] | [1] | 0.4444 | 0 | 3/4 · 0.4444 = 0.3333 |

3. The lowest score is `0` at threshold `2.5` on feature `0`.
4. Result: `[0, 2.5, 0.0]`, printed as `[0,2.50000,0.00000]`.

## Tools you'll need

### np.argsort(a, kind="stable")

- Returns the indices that would sort `a`.
- Use the same indices to reorder the labels along with the feature values.
- `kind="stable"` keeps equal values in their original order.

```python
import numpy as np
v = np.array([30, 10, 20])
order = np.argsort(v, kind="stable")
print(order)     # [1 2 0]
print(v[order])  # [10 20 30]
```

### One-hot encoding with broadcasting

- Comparing a column `(n, 1)` with a row `(1, C)` gives an `(n, C)` boolean table.
- Each row has a single `True`, in the column of that sample's class.
- `.astype(float)` turns it into 0/1 numbers.

```python
import numpy as np
y = np.array([2, 0, 2])
classes = np.unique(y)
print(classes)  # [0 2]
oh = (y[:, None] == classes[None, :]).astype(float)
print(oh.shape)  # (3, 2)
print(oh)
# [[0. 1.]
#  [1. 0.]
#  [0. 1.]]
```

### np.cumsum(a, axis=0)

- Running total down the rows.
- On one-hot rows, row `i` of the result is the class counts of the first `i + 1` samples.

```python
import numpy as np
a = np.array([[1, 0], [0, 1], [1, 0]])
print(np.cumsum(a, axis=0))
# [[1 0]
#  [1 1]
#  [2 1]]
```

### Comparing neighbours and np.nonzero

- `v[:-1] < v[1:]` compares each value with the next one.
- `np.nonzero(mask)[0]` gives the positions where the mask is `True`.
- Applied to sorted values, these are the places where the value changes.

```python
import numpy as np
v = np.array([1, 1, 2, 5, 5])
mask = v[:-1] < v[1:]
print(mask)                 # [False  True  True False]
print(np.nonzero(mask)[0])  # [1 2]
```

### Summing along an axis

- `(counts ** 2).sum(axis=1)` adds across classes, giving one result per row.
- Dividing a `(k, C)` array by `k` sizes needs a column: `size[:, None]`.

```python
import numpy as np
c = np.array([[3.0, 1.0], [2.0, 2.0]])
size = c.sum(axis=1)
p = c / size[:, None]
print(p.shape)                   # (2, 2)
print(1 - (p ** 2).sum(axis=1))  # [0.375 0.5  ]
```

## Common mistakes

- **Cutting between equal values.** Equal neighbours can't be separated by any threshold. Only cut where the sorted value strictly increases.
- **Off-by-one on the left size.** A cut after sorted index `i` leaves `i + 1` samples on the left, not `i`.
- **Wrong division shape.** Dividing `(k, C)` counts by a length-`k` vector fails or broadcasts the wrong way. Use `size[:, None]`.
- **Ignoring ties.** Scores within `1e-12` count as equal. Replace the best only if the new score is lower by more than `1e-12`, and scan features and thresholds in increasing order so the first one wins.
- **The no-split case.** If every feature is constant, return `[-1, 0.0, Gini(y)]`. Don't return an infinite starting score.

## Hints

### Hint 1

- Handle one feature at a time.
- Sort the samples by that feature.
- Find where the sorted value changes.
- For each such cut, get the class counts on the left and on the right.
- Compute the weighted Gini score for each cut.
- Keep the best across all features.
- If no cut was ever valid, return the fallback.

### Hint 2

- One-hot encode `y`: shape `(n, C)`.
- Sort with `np.argsort`, then reorder the feature values and one-hot rows together.
- `np.cumsum(..., axis=0)` gives left counts: shape `(n, C)`.
- Pick valid rows with `np.nonzero(v[:-1] < v[1:])[0]`: shape `(k,)`.
- Right counts are the total counts minus the left counts.
- Compute Gini per row with `.sum(axis=1)`: shape `(k,)`.

### Hint 3

- For a cut after sorted index `i`, the left size is `i + 1` and the right size is `n - (i + 1)`.
- The left counts are row `i` of the cumulative sum; the right counts are `total - left`.
- Gini of a side is `1 - sum((counts / size)²)` over classes.
- Score = `(n_left · Gini_left + n_right · Gini_right) / n`.
- The threshold is `(v[i] + v[i+1]) / 2`.
- Loop over features in order, then cuts in increasing order.
- Update the best only when `score < best_score - 1e-12`.
