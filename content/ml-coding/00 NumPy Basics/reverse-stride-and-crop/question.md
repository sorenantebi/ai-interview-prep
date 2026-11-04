---
topic: "NumPy Basics"
difficulty: Easy
---
# Reverse, Stride and Crop

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

Practise **basic slicing** on a 2-D array. Write a function `slice_views(a, r0, r1, c0, c1)` that receives a 2-D float array `a` of shape `(n, m)` and four integers describing a block, and returns a tuple `(flipped, block)` of two arrays:

- `flipped`: `a` with the **rows in reverse order** and only **every other column** kept (columns `0, 2, 4, ...`). Practise the step slice `a[::-1, ::2]`.
- `block`: the sub-block made of rows `r0` up to (not including) `r1` and columns `c0` up to (not including) `c1`. Practise `a[r0:r1, c0:c1]`.

The solution is one or two lines. No loops are needed.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: a = [[1.0,2.0,3.0,4.0],[5.0,6.0,7.0,8.0],[9.0,10.0,11.0,12.0]], r0 = 1, r1 = 3, c0 = 1, c1 = 3
Output: ([[9.00000,11.00000],[5.00000,7.00000],[1.00000,3.00000]],[[6.00000,7.00000],[10.00000,11.00000]])
Explanation: Reversing the rows gives [9..12], [5..8], [1..4]; keeping columns 0 and 2 gives the first array. The block is rows 1-2 and columns 1-2 of the original.
```

**Example 2**
```text
Input: a = [[1.0,2.0],[3.0,4.0]], r0 = 0, r1 = 1, c0 = 0, c1 = 2
Output: ([[3.00000],[1.00000]],[[1.00000,2.00000]])
```

**Example 3**
```text
Input: a = [[7.0]], r0 = 0, r1 = 1, c0 = 0, c1 = 1
Output: ([[7.00000]],[[7.00000]])
```

## Constraints

- `1 <= n, m <= 10^3`
- `0 <= r0 < r1 <= n` and `0 <= c0 < c1 <= m`, so the block is never empty
