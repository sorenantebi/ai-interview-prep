---
topic: "ML From Scratch"
difficulty: Hard
---
# Decision Stump: Best Gini Split

**Topic:** ML From Scratch · **Difficulty:** Hard

## Problem

Find the single split that a decision tree would choose at its root, using Gini impurity.

`X` has shape `(n, d)` and `y` holds `n` integer class labels. A split is a feature `f` and a threshold `t`: samples with `X[i, f] <= t` go left, the rest go right.

- **Candidate thresholds** for feature `f` are the midpoints between consecutive distinct values of that feature, after sorting. So a feature with values `{1, 2, 4}` has candidates `1.5` and `3.0`. Constant features have no candidates.
- **Gini impurity** of a set of labels is `1 - Σ_c p_c²`, where `p_c` is the fraction of labels equal to `c`.
- **Score** of a split = `(n_left / n) · Gini(left) + (n_right / n) · Gini(right)`. Lower is better.

Return `[feature, threshold, score]` for the split with the lowest score. If several splits tie (scores within `1e-12` of each other), choose the smallest feature index, then the smallest threshold. If no feature has a candidate threshold, return `[-1, 0.0, Gini(y)]`.

## Examples

**Example 1**
```text
Input: X = [[1.0], [2.0], [3.0], [4.0]], y = [0, 0, 1, 1]
Output: [0,2.50000,0.00000]
```

**Example 2**
```text
Input: X = [[1.0, 5.0], [2.0, 5.0], [3.0, 6.0], [4.0, 6.0], [5.0, 7.0]], y = [0, 1, 0, 1, 1]
Output: [0,3.50000,0.26667]
```

**Example 3**
```text
Input: X = [[3.0], [3.0]], y = [0, 1]
Output: [-1,0.00000,0.50000]
```

## Constraints

- `1 <= n <= 2000`
- `1 <= d <= 20`
- `0 <= y[i] < 50`
