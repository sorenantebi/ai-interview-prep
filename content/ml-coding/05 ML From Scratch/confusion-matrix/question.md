---
topic: "ML From Scratch"
difficulty: Easy
---
# Confusion Matrix

**Topic:** ML From Scratch · **Difficulty:** Easy

## Problem

You are given the true labels `y_true` and the predicted labels `y_pred` of `n` samples, both 1-D integer arrays with values in `0 .. num_classes - 1`.

Return the confusion matrix as an integer array of shape `(num_classes, num_classes)`, where entry `[i, j]` counts the samples whose true label is `i` and whose predicted label is `j`. Rows are true classes, columns are predicted classes. Classes that never appear still get their (all-zero) row and column.

## Examples

**Example 1**
```text
Input: y_true = [0, 1, 2, 1], y_pred = [0, 2, 2, 1], num_classes = 3
Output: [[1,0,0],[0,1,1],[0,0,1]]
```

**Example 2**
```text
Input: y_true = [1, 1, 0], y_pred = [0, 0, 0], num_classes = 2
Output: [[1,0],[2,0]]
```

## Constraints

- `1 <= n <= 10^5`
- `1 <= num_classes <= 100`
- `0 <= y_true[i], y_pred[i] < num_classes`
- Return an integer dtype array.
