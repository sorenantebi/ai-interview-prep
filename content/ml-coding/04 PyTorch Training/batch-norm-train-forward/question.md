---
topic: "PyTorch Training"
difficulty: Medium
---
# Batch Norm Training Forward

**Topic:** PyTorch Training · **Difficulty:** Medium

## Problem

Batch normalisation (in training mode) normalises each feature over the batch. Given `x` of shape `(n, d)`,
`gamma`, `beta`, `running_mean` and `running_var` (all shape `(d,)`), a `momentum` and an `eps`:

1. For each feature `j`, compute the batch mean `μ_j` and the *biased* batch variance `σ²_j` (divide by `n`).
2. Output `y[i, j] = (x[i, j] - μ_j) / sqrt(σ²_j + eps) * gamma[j] + beta[j]`.
3. Update the running statistics the way `nn.BatchNorm1d` does:
   `new_mean = (1 - momentum) · running_mean + momentum · μ` and
   `new_var = (1 - momentum) · running_var + momentum · s²`, where `s²` is the *unbiased* batch variance
   (divide by `n - 1`).

Return `[y, new_mean, new_var]`. Don't modify any input, and don't use `F.batch_norm` or `nn.BatchNorm1d`.

## Examples

**Example 1**
```text
Input: x = [[1.0, 2.0], [3.0, 6.0]], gamma = [1.0, 1.0], beta = [0.0, 0.0], running_mean = [0.0, 0.0], running_var = [1.0, 1.0], momentum = 0.1, eps = 1e-5
Output: [[[-0.99999,-1.00000],[0.99999,1.00000]],[0.20000,0.40000],[1.10000,1.70000]]
Explanation: the batch means are [2, 4]; the unbiased variances are [2, 8], so the running variance moves from 1 to 0.9 + 0.1 · [2, 8].
```

**Example 2**
```text
Input: x = [[0.0], [0.0], [3.0]], gamma = [2.0], beta = [1.0], running_mean = [1.0], running_var = [0.5], momentum = 0.5, eps = 1e-5
Output: [[[-0.41421],[-0.41421],[3.82842]],[1.00000],[1.75000]]
```

## Constraints

- `2 <= n <= 10^4`, `1 <= d <= 1024`
- `0 <= momentum <= 1`, `0 < eps <= 0.1`
