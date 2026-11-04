---
topic: "NumPy Basics"
difficulty: Easy
---
# Row, Column and Overall Aggregates

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

This is a fundamentals drill on NumPy reductions and the `axis=` argument. The practice calls are `sum`, `mean`, `max` and `argmax`.

Write a function `aggregate_stats(x)` that receives a 2D float array `x` of shape `(n, d)` and returns a tuple of four values:

1. the **row sums**: a 1D array of shape `(n,)` with the sum of each row (`sum` with `axis=1`),
2. the **column means**: a 1D array of shape `(d,)` with the mean of each column (`mean` with `axis=0`),
3. the **overall maximum**: a single float, the largest entry of the whole array (`max` without an axis),
4. the **argmax of each column**: a 1D integer array of shape `(d,)` holding, for every column, the row index of its largest entry (`argmax` with `axis=0`). If a column has ties, return the first (smallest) row index.

The intended solution is one line per value. No Python loops are needed.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
Output: [[6.00000,15.00000],[2.50000,3.50000,4.50000],6.00000,[1,1,1]]
Explanation: Row sums are 1+2+3 and 4+5+6. Column means are (1+4)/2, (2+5)/2, (3+6)/2. The largest entry is 6, and every column peaks in row 1.
```

**Example 2**
```text
Input: x = [[3.0, -1.0], [0.0, 7.0], [3.0, 2.0]]
Output: [[2.00000,7.00000,5.00000],[2.00000,2.66667],7.00000,[0,1]]
Explanation: Column 0 is [3, 0, 3]: the maximum 3 appears in rows 0 and 2, so the first index 0 is returned.
```

**Example 3**
```text
Input: x = [[-2.5]]
Output: [[-2.50000],[-2.50000],-2.50000,[0]]
```

## Constraints

- `1 <= n, d <= 10^3`
- `x` is a 2D float array without NaN values
