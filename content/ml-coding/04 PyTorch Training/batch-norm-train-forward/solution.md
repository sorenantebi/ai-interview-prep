---
topic: "PyTorch Training"
difficulty: Medium
---
# Batch Norm Training Forward - Solution

## Intuition

Statistics run down the batch dimension (`dim=0`), one per feature. The output uses the biased variance because it describes this exact batch, while the running variance is an estimate of the population variance and so uses the unbiased one, which is what PyTorch does.

## Approach

1. `mean = x.mean(dim=0)`, `var = x.var(dim=0, unbiased=False)`.
2. `y = (x - mean) / torch.sqrt(var + eps) * gamma + beta`.
3. `unbiased = x.var(dim=0, unbiased=True)`.
4. Blend the running statistics with `momentum` into new tensors and return the three results.

## Code

```python
import torch

def batch_norm_train(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, running_mean: torch.Tensor,
                     running_var: torch.Tensor, momentum: float, eps: float) -> list:
    mean = x.mean(dim=0)
    var = x.var(dim=0, unbiased=False)
    y = (x - mean) / torch.sqrt(var + eps) * gamma + beta
    new_mean = (1 - momentum) * running_mean + momentum * mean
    new_var = (1 - momentum) * running_var + momentum * x.var(dim=0, unbiased=True)
    return [y, new_mean, new_var]
```

## Complexity

- **Time:** `O(n·d)` — a few passes over `x`.
- **Space:** `O(n·d)` — the normalised output.
