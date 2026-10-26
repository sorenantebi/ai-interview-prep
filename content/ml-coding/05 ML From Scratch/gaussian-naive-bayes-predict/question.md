---
topic: "ML From Scratch"
difficulty: Medium
---
# Gaussian Naive Bayes

**Topic:** ML From Scratch · **Difficulty:** Medium

## Problem

Fit a Gaussian naive Bayes classifier on training data and predict labels for test data.

`X_train` has shape `(m, d)` with integer labels `y_train`, and `X_test` has shape `(q, d)`. For every class `c` that appears in `y_train`:

- the prior is `P(c) = (number of training samples of class c) / m`;
- each feature `j` has mean `μ[c, j]` and variance `σ²[c, j]` over that class's samples, where the variance is the population variance (divide by the count, not count − 1) **plus `eps`**, which keeps constant features from giving zero variance.

A test point `x` scores each class with

`log P(c) + Σ_j log N(x_j; μ[c, j], σ²[c, j])`, where `log N(x; μ, σ²) = -½·log(2π·σ²) - (x - μ)² / (2σ²)`.

Predict the class with the highest score; if classes tie, predict the smallest label. Return the predicted labels (values from `y_train`) as an integer array of shape `(q,)`.

## Examples

**Example 1**
```text
Input: X_train = [[1.0], [2.0], [8.0], [9.0]], y_train = [0, 0, 1, 1], X_test = [[1.5], [7.0], [5.0]], eps = 1e-9
Output: [0,1,0]
```

**Example 2**
```text
Input: X_train = [[0.0, 1.0], [1.0, 1.0], [5.0, 3.0], [6.0, 3.0], [6.0, 4.0]], y_train = [3, 3, 7, 7, 7], X_test = [[0.5, 1.0], [5.0, 2.0]], eps = 0.01
Output: [3,7]
```

## Constraints

- `1 <= m, q <= 5000`
- `1 <= d <= 50`
- at most 20 classes
- `eps > 0`
