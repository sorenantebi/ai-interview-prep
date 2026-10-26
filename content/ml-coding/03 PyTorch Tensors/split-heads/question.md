---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Split and Merge Heads

**Topic:** PyTorch Tensors · **Difficulty:** Medium

## Problem

Multi-head attention works on `num_heads` slices of the model dimension in parallel. Write the reshaping in both directions:

- `split = True`: `x` has shape `(B, T, D)` with `D` divisible by `num_heads`. Return shape `(B, num_heads, T, D / num_heads)`, where head `h` gets features `h·dh … (h+1)·dh - 1` (`dh = D / num_heads`).
- `split = False`: `x` has shape `(B, num_heads, T, dh)`. Return shape `(B, T, num_heads·dh)`, the exact inverse of splitting.

Don't use Python loops.

## Examples

**Example 1**
```text
Input: x = [[[1, 2, 3, 4], [5, 6, 7, 8]]], num_heads = 2, split = true
Output: [[[[1,2],[5,6]],[[3,4],[7,8]]]]
Explanation: Head 0 gets features 0-1 of each token, head 1 features 2-3.
```

**Example 2**
```text
Input: x = [[[[1, 2], [5, 6]], [[3, 4], [7, 8]]]], num_heads = 2, split = false
Output: [[[1,2,3,4],[5,6,7,8]]]
Explanation: Merging puts the heads back side by side.
```

## Constraints

- `1 <= B, T <= 512`, `1 <= num_heads <= D <= 1024`
- Splitting then merging must return the original tensor
