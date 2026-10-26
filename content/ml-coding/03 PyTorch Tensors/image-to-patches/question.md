---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Image to Patches

**Topic:** PyTorch Tensors · **Difficulty:** Medium

## Problem

A Vision Transformer cuts each image into non-overlapping `patch × patch` squares and flattens each square into a vector. `images` has shape `(B, C, H, W)` with `H` and `W` divisible by `patch`.

Return a tensor of shape `(B, N, C·patch·patch)` with `N = (H/patch)·(W/patch)`:
- patches are ordered row-major over the patch grid (left to right, then top to bottom);
- each patch vector lists channel 0's `patch × patch` pixels row by row, then channel 1's, and so on (the patch's `(C, patch, patch)` block, flattened).

Keep the dtype and don't use Python loops.

## Examples

**Example 1**
```text
Input: images = [[[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]]], patch = 2
Output: [[[0,1,4,5],[2,3,6,7],[8,9,12,13],[10,11,14,15]]]
Explanation: A 4×4 single-channel image gives a 2×2 grid of patches.
```

**Example 2**
```text
Input: images = [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]], patch = 2
Output: [[[1,2,3,4,5,6,7,8]]]
Explanation: One patch: channel 0's pixels, then channel 1's.
```

## Constraints

- `1 <= B, C <= 64`, `1 <= patch <= H, W <= 512`
- `H % patch == 0` and `W % patch == 0`
