---
topic: "NumPy Basics"
difficulty: Easy
---
# Framed Matrix with a Diagonal

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

Write a function `framed_matrix(n, value)` that returns an `n x n` float array with this layout:

- the **border** (first row, last row, first column, last column) is `1`
- the **inside** (everything not on the border) is `0`
- the **main diagonal** is `value`. The diagonal wins wherever it overlaps the border, so the corners on the diagonal are also `value`.

This is a drill on creating arrays. Practise these calls: `np.zeros`, `np.ones`, `np.full` and `np.eye`. The intended solution is only 1-3 lines, with no Python loops.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: n = 3, value = 5.0
Output: [[5.00000,1.00000,1.00000],[1.00000,5.00000,1.00000],[1.00000,1.00000,5.00000]]
Explanation: the only inner cell is the centre, which is on the diagonal.
```

**Example 2**
```text
Input: n = 4, value = 7.0
Output: [[7.00000,1.00000,1.00000,1.00000],[1.00000,7.00000,0.00000,1.00000],[1.00000,0.00000,7.00000,1.00000],[1.00000,1.00000,1.00000,7.00000]]
```

**Example 3**
```text
Input: n = 1, value = 2.0
Output: [[2.00000]]
Explanation: the single cell is border and diagonal at once, so the diagonal value wins.
```

## Constraints

- `1 <= n <= 10^3`
- `value` is a finite float
