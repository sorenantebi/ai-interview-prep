---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Sinusoidal Positional Encoding

**Topic:** PyTorch Tensors · **Difficulty:** Medium

## Problem

Return the fixed sinusoidal positional encoding from the original Transformer: a `float32` tensor `pe` of shape `(seq_len, d_model)` where, for position `p` and `i = 0 .. d_model/2 - 1`:

- `pe[p, 2i]   = sin(p / 10000^(2i / d_model))`
- `pe[p, 2i+1] = cos(p / 10000^(2i / d_model))`

Even columns hold sines and odd columns cosines, and each sine/cosine pair shares one frequency. Don't use Python loops.

## Examples

**Example 1**
```text
Input: seq_len = 2, d_model = 4
Output: [[0.00000,1.00000,0.00000,1.00000],[0.84147,0.54030,0.01000,0.99995]]
Explanation: Position 0 is always [0, 1, 0, 1, ...]. The second pair's frequency is 10000^(-2/4) = 0.01.
```

**Example 2**
```text
Input: seq_len = 3, d_model = 2
Output: [[0.00000,1.00000],[0.84147,0.54030],[0.90930,-0.41615]]
```

## Constraints

- `1 <= seq_len <= 4096`
- `2 <= d_model <= 1024`, `d_model` is even
- The result's dtype is `torch.float32`
