---
topic: "ML From Scratch"
difficulty: Hard
---
# Ridge Regression (Closed Form)

**Topic:** ML From Scratch · **Difficulty:** Hard

## Problem

Fit ridge regression with an intercept, in closed form, **without penalising the intercept**.

`X` has shape `(n, d)` and `y` has shape `(n,)`. Find `w` of shape `(d + 1,)`, intercept first, that minimises

`||A w - y||² + alpha · Σ_{j=1..d} w[j]²`

where `A` is `X` with a column of ones put in front. Note the penalty sum starts at `j = 1`: `w[0]`, the intercept, is not shrunk.

`alpha > 0`, so the solution is unique even when columns are duplicated or `n < d`.

## Examples

**Example 1**
```text
Input: X = [[1.0], [2.0], [3.0]], y = [3.0, 5.0, 7.0], alpha = 1.0
Output: [2.33333,1.33333]
```

**Example 2**
```text
Input: X = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 2.0]], y = [2.0, 1.0, 4.0, 7.0], alpha = 0.5
Output: [0.35714,1.90476,1.23810]
```

## Constraints

- `1 <= n <= 10^4`
- `1 <= d <= 100`
- `0 < alpha <= 10^6`
