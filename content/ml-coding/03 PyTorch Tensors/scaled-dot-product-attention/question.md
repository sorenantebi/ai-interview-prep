---
topic: "PyTorch Tensors"
difficulty: Hard
---
# Scaled Dot-Product Attention

**Topic:** PyTorch Tensors · **Difficulty:** Hard

## Problem

Implement scaled dot-product attention. `q` has shape `(B, Tq, d)`, `k` has shape `(B, Tk, d)` and `v` has shape `(B, Tk, dv)` (float). `mask` is optional: `None`, or a boolean tensor of shape `(B, Tq, Tk)` where `True` means query `i` may attend to key `j`.

Return `softmax(q·kᵀ / sqrt(d)) · v` with shape `(B, Tq, dv)`, where the softmax runs over the keys and only over the allowed keys (disallowed keys get weight 0). A query with no allowed key at all returns a row of zeros.

It must stay correct for very large scores (e.g. `q` entries around 1000), and the result must never contain `nan`. Don't use `F.scaled_dot_product_attention` or `nn.MultiheadAttention` (the hidden tests disable them).

## Examples

**Example 1**
```text
Input: q = [[[1.0, 0.0]]], k = [[[1.0, 0.0], [0.0, 1.0]]], v = [[[10.0], [20.0]]], mask = [[[true, true]]]
Output: [[[13.30239]]]
Explanation: The scores are 1/sqrt(2) and 0, so the first key gets the larger weight.
```

**Example 2**
```text
Input: q = [[[1.0, 0.0], [0.0, 1.0]]], k = [[[1.0, 0.0], [0.0, 1.0]]], v = [[[10.0], [20.0]]], mask = [[[true, false], [false, false]]]
Output: [[[10.00000],[0.00000]]]
Explanation: Query 0 may only see key 0. Query 1 sees no key, so its output is 0.
```

## Constraints

- `1 <= B <= 16`, `1 <= Tq, Tk <= 512`, `1 <= d, dv <= 128`
- Inputs are finite; scores can be as large as `10^6`
