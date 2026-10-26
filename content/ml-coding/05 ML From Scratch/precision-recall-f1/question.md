---
topic: "ML From Scratch"
difficulty: Easy
---
# Precision, Recall and F1

**Topic:** ML From Scratch · **Difficulty:** Easy

## Problem

You are given the true labels `y_true` and the predicted labels `y_pred` of a binary classifier, both 1-D arrays of 0s and 1s. Class `1` is the positive class.

Return `[precision, recall, f1]` as a list of three floats:

- `precision = TP / (TP + FP)`
- `recall = TP / (TP + FN)`
- `f1 = 2 · precision · recall / (precision + recall)`

Whenever a denominator is 0 (no predicted positives, no actual positives, or `precision + recall == 0`), that value is `0.0`.

## Examples

**Example 1**
```text
Input: y_true = [1, 0, 1, 1, 0], y_pred = [1, 1, 0, 1, 0]
Output: [0.66667,0.66667,0.66667]
```

**Example 2**
```text
Input: y_true = [0, 0, 1], y_pred = [0, 0, 0]
Output: [0.00000,0.00000,0.00000]
```

## Constraints

- `1 <= n <= 10^5`
- `y_true[i], y_pred[i]` are 0 or 1
