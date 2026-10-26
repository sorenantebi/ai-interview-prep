---
topic: "ML From Scratch"
difficulty: Medium
---
# K-Nearest Neighbours Classifier

**Topic:** ML From Scratch · **Difficulty:** Medium

## Problem

Classify each test point by a majority vote of its `k` nearest training points.

`X_train` has shape `(m, d)` with integer labels `y_train` of shape `(m,)`, and `X_test` has shape `(q, d)`. For each test point:

1. Find the `k` training points with the smallest Euclidean distance. If several training points are equally far, the one with the smaller index counts as closer.
2. Predict the label that appears most often among those `k` neighbours. If several labels tie for most votes, predict the smallest of them.

Return the predictions as an integer array of shape `(q,)`.

## Examples

**Example 1**
```text
Input: X_train = [[0.0, 0.0], [1.0, 0.0], [5.0, 5.0], [6.0, 5.0]], y_train = [0, 0, 1, 1], X_test = [[0.5, 0.5], [5.5, 4.0]], k = 3
Output: [0,1]
```

**Example 2**
```text
Input: X_train = [[0.0], [2.0], [3.0], [10.0]], y_train = [4, 1, 4, 1], X_test = [[1.0], [2.5]], k = 2
Output: [1,1]
```

## Constraints

- `1 <= m, q <= 2000`
- `1 <= k <= m`
- `0 <= y_train[i] <= 1000`
