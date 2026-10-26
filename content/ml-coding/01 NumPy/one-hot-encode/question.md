---
topic: "NumPy"
difficulty: Easy
---
# One-Hot Encode

**Topic:** NumPy · **Difficulty:** Easy

## Problem

Given a 1-D integer array `labels` of length `n` with every value in `[0, num_classes)`, return an integer array of shape `(n, num_classes)` where row `i` is all zeros except for a `1` in column `labels[i]`.

Build the result without a Python loop over the labels. An empty `labels` array gives an array of shape `(0, num_classes)`.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: labels = [0, 2, 1], num_classes = 3
Output: [[1,0,0],[0,0,1],[0,1,0]]
```

**Example 2**
```text
Input: labels = [1, 1], num_classes = 4
Output: [[0,1,0,0],[0,1,0,0]]
```

## Constraints

- `0 <= n <= 10^6`
- `1 <= num_classes <= 1000`
- `0 <= labels[i] < num_classes`
