---
topic: "NumPy"
difficulty: Easy
---
# Moving Average

**Topic:** NumPy · **Difficulty:** Easy

## Problem

Given a 1-D float array `x` of length `n` and a window size `k` (`1 <= k <= n`), return the mean of every window of `k` consecutive values: an array of length `n - k + 1` whose element `i` is `mean(x[i : i + k])`.

Solve it in `O(n)` time without a Python loop over the windows (hint: a cumulative sum gives every window sum at once).

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [1.0, 2.0, 3.0, 4.0, 5.0], k = 2
Output: [1.50000,2.50000,3.50000,4.50000]
```

**Example 2**
```text
Input: x = [4.0, 0.0, 8.0], k = 3
Output: [4.00000]
```

## Constraints

- `1 <= k <= n <= 10^6`
- `-10^3 <= x[i] <= 10^3`
