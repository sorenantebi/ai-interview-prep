---
topic: "ML From Scratch"
difficulty: Easy
---
# Linear Regression (Normal Equation)

**Topic:** ML From Scratch · **Difficulty:** Easy

## Problem

Fit an ordinary least-squares linear regression with an intercept, in closed form.

`X` has shape `(n, d)` (one row per sample) and `y` has shape `(n,)`. Find weights `w` of shape `(d + 1,)` that minimise `||A w - y||²`, where `A` is `X` with a column of ones put in front. So `w[0]` is the intercept (bias) and `w[1:]` are the feature weights.

If the least-squares solution is not unique (for example, duplicate columns, or fewer samples than weights), return the one with the smallest norm `||w||`. This is what `np.linalg.lstsq` and the pseudo-inverse give; inverting `AᵀA` directly fails in that case.

## Examples

**Example 1**
```text
Input: X = [[1.0], [2.0], [3.0]], y = [3.0, 5.0, 7.0]
Output: [1.00000,2.00000]
```

**Example 2**
```text
Input: X = [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [2.0, 1.0]], y = [1.0, 2.0, 2.5, 4.0]
Output: [0.50000,1.50000,0.50000]
```

## Constraints

- `1 <= n <= 10^4`
- `1 <= d <= 50`
- Return a float array of shape `(d + 1,)`
