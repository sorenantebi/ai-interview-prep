---
topic: "PyTorch Training"
difficulty: Medium
---
# Layer Norm Forward

**Topic:** PyTorch Training · **Difficulty:** Medium

## Problem

Layer normalisation normalises each example over its features. Given `x` of shape `(n, d)`, a scale `gamma`
and a shift `beta` (both shape `(d,)`) and a small constant `eps`, return

`y[i, j] = (x[i, j] - mean_i) / sqrt(var_i + eps) * gamma[j] + beta[j]`

where `mean_i` and `var_i` are the mean and the *biased* variance (divide by `d`) of row `i`. Don't use
`F.layer_norm` or `nn.LayerNorm`.

## Examples

**Example 1**
```text
Input: x = [[1.0, 2.0, 3.0]], gamma = [1.0, 1.0, 1.0], beta = [0.0, 0.0, 0.0], eps = 1e-5
Output: [[-1.22474,0.00000,1.22474]]
```

**Example 2**
```text
Input: x = [[2.0, 2.0], [0.0, 4.0]], gamma = [2.0, 1.0], beta = [0.5, -0.5], eps = 1e-5
Output: [[0.50000,-0.50000],[-1.50000,0.50000]]
Explanation: the first row is constant, so it normalises to 0 and only beta remains.
```

## Constraints

- `1 <= n <= 10^4`, `1 <= d <= 2048`
- `0 < eps <= 0.1`
