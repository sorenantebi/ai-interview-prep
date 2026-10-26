---
topic: "ML From Scratch"
difficulty: Medium
---
# ROC AUC

**Topic:** ML From Scratch · **Difficulty:** Medium

## Problem

Compute the area under the ROC curve of a binary classifier.

`y_true` holds the labels (0 or 1) and `scores` the classifier's scores, higher meaning "more likely positive". Both have shape `(n,)`, and both classes appear at least once.

The AUC equals the probability that a randomly chosen positive gets a higher score than a randomly chosen negative, counting a tie as one half:

`AUC = (#pairs with pos > neg + 0.5 · #pairs with pos == neg) / (#positives · #negatives)`

over all (positive, negative) pairs. Return it as a float.

Follow-up: can you do it in `O(n log n)` instead of comparing every pair?

## Examples

**Example 1**
```text
Input: y_true = [0, 0, 1, 1], scores = [0.1, 0.4, 0.35, 0.8]
Output: 0.75000
```

**Example 2**
```text
Input: y_true = [1, 0, 1, 0], scores = [0.5, 0.5, 0.9, 0.2]
Output: 0.87500
```

## Constraints

- `2 <= n <= 10^5`
- both classes are present
