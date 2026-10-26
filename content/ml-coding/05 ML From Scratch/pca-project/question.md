---
topic: "ML From Scratch"
difficulty: Medium
---
# PCA Projection

**Topic:** ML From Scratch · **Difficulty:** Medium

## Problem

Project data onto its top `k` principal components.

`X` has shape `(n, d)`. Center the data by subtracting each column's mean. The principal components are the unit-length eigenvectors of the covariance matrix of the centered data, ordered by decreasing eigenvalue (variance). Return the centered data projected onto the first `k` of them: an array of shape `(n, k)` whose column `j` is the centered data times component `j`.

An eigenvector's sign is arbitrary, so fix it: flip each component so that its entry with the largest absolute value is positive (if several entries tie, use the first one).

The tests only use data whose top `k + 1` variances are distinct, so the components are unique up to sign.

## Examples

**Example 1**
```text
Input: X = [[1.0, 2.0], [3.0, 3.0], [5.0, 7.0]], k = 1
Output: [[-2.79845],[-0.80229],[3.60074]]
```

**Example 2**
```text
Input: X = [[2.0, 0.0, 1.0], [0.0, 1.0, 1.0], [4.0, 1.0, 0.0], [2.0, 2.0, 2.0]], k = 2
Output: [[0.04459,-0.80410],[-1.90882,-0.41922],[2.20397,-0.13710],[-0.33974,1.36042]]
```

## Constraints

- `2 <= n <= 5000`
- `1 <= k <= d <= 50`
