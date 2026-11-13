# Learn: ROC AUC

## The idea

- **Classifier score**: a number per example; higher means "more likely positive".
- **ROC curve**: a plot of how well those scores separate the classes as you slide a decision threshold.
- **AUC** (area under the ROC curve): that plot squeezed into one number between 0 and 1.
- It shows up in evaluation reports because it doesn't depend on one chosen threshold.
- Intuition, no curve needed: pick one random positive and one random negative.
  - A good classifier gives the positive the higher score.
  - AUC is the probability that this happens.
- Reading the number:
  - 1.0 means every positive outranks every negative.
  - 0.5 means the scores are no better than coin flips.
- **Tie**: two equal scores in a (positive, negative) pair. It counts as half a win.
- So the task is to score every (positive, negative) pair as win (1), tie (0.5) or loss (0).
  - Add the points up, then divide by `#positives · #negatives`.
- **Rank**: the position of a score in sorted order, starting at 1.
  - Tied scores share the average of the ranks they occupy, e.g. two scores tied for ranks 2 and 3 both get 2.5.
- The `O(n log n)` follow-up uses ranks: sort once instead of comparing every pair.

## Work it by hand

Example 1: `y_true = [0, 0, 1, 1]`, `scores = [0.1, 0.4, 0.35, 0.8]`.

- There are 2 positives (scores 0.35 and 0.8) and 2 negatives (scores 0.1 and 0.4), so 2 · 2 = 4 pairs.

| positive score | negative score | result | points |
|---|---|---|---|
| 0.35 | 0.1 | win | 1 |
| 0.35 | 0.4 | loss | 0 |
| 0.8 | 0.1 | win | 1 |
| 0.8 | 0.4 | win | 1 |

- Total = 3 points, so AUC = 3 / 4 = **0.75**.

Now the rank way, with no pair loop:

1. Sort the scores: `0.1, 0.35, 0.4, 0.8`. Their ranks are 1, 2, 3, 4.
2. Put the ranks back in the original order: 0.1 → 1, 0.4 → 3, 0.35 → 2, 0.8 → 4, so the ranks array is `[1, 3, 2, 4]`.
3. The positives are at positions 2 and 3, with ranks 2 and 4. Their sum is 6.
4. A positive's rank counts every score below it, but that includes the other positives and itself.
   - With P = 2 positives, that unwanted part is `P·(P+1)/2 = 3`.
   - Winning pairs = 6 − 3 = 3.
5. AUC = 3 / (P · N) = 3 / 4 = **0.75**. Both methods agree.

## Tools you'll need

### np.argsort(a)
- Returns the indices that would sort `a`, not the sorted values.
- `kind="stable"` keeps equal values in their original order.

```python
import numpy as np
a = np.array([30, 10, 20])
print(np.argsort(a))  # [1 2 0]
print(a[np.argsort(a)])  # [10 20 30]
```

### Boolean masks
- A comparison like `y == 1` gives a boolean array of the same shape.
- Index with it to pick elements, use `.sum()` to count the `True` values, and `~mask` to flip it.

```python
import numpy as np
y = np.array([1, 0, 0, 1, 1])
v = np.array([5., 6., 7., 8., 9.])
m = y == 1
print(v[m])  # [5. 8. 9.]
print(m.sum(), (~m).sum())  # 3 2
```

### Assigning through index arrays
- `out[idx] = values` writes each value at the position given in `idx`.
- That is how you put values computed in sorted order back into the original order.

```python
import numpy as np
order = np.array([2, 0, 1])
out = np.empty(3)
out[order] = [1., 2., 3.]
print(out)  # [2. 3. 1.]
```

### Slice assignment
- `r[i:j] = x` sets a whole run of positions to one number.
- The end index `j` is excluded.
- This is handy for giving a tied run the same rank.

```python
import numpy as np
r = np.zeros(5)
r[1:4] = 2.5
print(r)  # [0.  2.5 2.5 2.5 0. ]
```

### np.unique(a, return_inverse=True, return_counts=True)
- Returns the sorted distinct values, which distinct value each element maps to, and how often each appears.
- It can help find ties without a manual loop.

```python
import numpy as np
a = np.array([3, 1, 3, 2])
u, inv, cnt = np.unique(a, return_inverse=True, return_counts=True)
print(u, inv, cnt)  # [1 2 3] [2 0 2 1] [1 1 2]
```

## Common mistakes

- **Ignoring ties.** Ranks 1, 2 for two equal scores instead of 1.5, 1.5 changes the answer.
  - Average the ranks of each tied group.
- **Starting ranks at 0.** The correction `P·(P+1)/2` assumes ranks start at 1.
  - With 0-based ranks the result is off.
- **Integer division.** Use `/`, not `//`, and return a plain `float`.
- **Mixing sorted order with original order.** Ranks must be placed back at the original positions before you select positives with `y_true == 1`.
  - Alternatively, reorder `y_true` by the same sort. Just don't mix the two.
- **Modifying the inputs.** Don't sort `scores` or `y_true` in place. Use `argsort` or work on copies.

## Hints

### Hint 1
- Sort the scores and give each a rank from 1 to n.
- Where scores tie, give the whole tied group the average of its ranks.
- Add up the ranks of the positive examples only.
- Subtract the part that comes from positives being ranked above each other and themselves.
- Divide by the number of (positive, negative) pairs.

### Hint 2
- Get the sorted order with `np.argsort`, giving an index array of shape `(n,)`.
- Walk through the sorted scores to find runs of equal values.
- Assign each run its average rank into a ranks array of shape `(n,)`, indexed in the original order.
- Select the positives' ranks with the mask `y_true == 1`, then sum them to get a single number.
- Count `P` and `N` from the mask.

### Hint 3
- If a tied run covers sorted positions `i` to `j` (0-based), the 1-based ranks are `i+1` through `j+1`.
  - Their average is `(i + j) / 2 + 1`, which every member of the run gets.
- Winning pairs: `U = (sum of positive ranks) - P·(P+1)/2`.
- Answer: `U / (P · N)`, where `P` and `N` are the counts of positives and negatives.
