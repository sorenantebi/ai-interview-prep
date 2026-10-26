---
topic: "PyTorch Training"
difficulty: Easy
---
# Linear Layer Forward - Solution

## Intuition

Stacking the rows of `x` turns the per-example product `W x_i` into one matrix product: row `i` of `x @ W.T` is exactly `W x_i`. The bias is the same for every example, so broadcasting adds it to every row.

## Approach

1. Multiply `x` (n × d_in) by `W.T` (d_in × d_out) to get an (n × d_out) matrix.
2. Add `b`; its shape `(d_out,)` broadcasts across the `n` rows.

## Code

```python
import torch

def linear(x: torch.Tensor, W: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    return x @ W.T + b
```

## Complexity

- **Time:** `O(n·d_in·d_out)` — one matrix product.
- **Space:** `O(n·d_out)` — the output.
