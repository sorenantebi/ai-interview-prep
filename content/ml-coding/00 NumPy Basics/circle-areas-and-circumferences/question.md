---
topic: "NumPy Basics"
difficulty: Easy
---
# Circle Areas and Circumferences

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

This is a fundamentals drill: practise `np.pi`, the `**` operator and `np.vstack`.

Write a function `circle_stats(radii)` that receives a 1-D NumPy array `radii` of length `n` (non-negative radii) and returns a 2-D array of shape `(2, n)`:

- row 0 holds the circle **areas**, `pi * r ** 2`
- row 1 holds the circle **circumferences**, `2 * pi * r`

Apply the formulas to the whole array at once (no Python loops), and stack the two result rows with `np.vstack`.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: radii = [1.0, 2.0]
Output: [[3.14159,12.56637],[6.28319,12.56637]]
Explanation: areas are pi*1 and pi*4; circumferences are 2*pi*1 and 2*pi*2.
```

**Example 2**
```text
Input: radii = [0.0]
Output: [[0.00000],[0.00000]]
```

**Example 3**
```text
Input: radii = [0.5, 1.5, 3.0]
Output: [[0.78540,7.06858,28.27433],[3.14159,9.42478,18.84956]]
```

## Constraints

- `1 <= n <= 10^5`
- `0 <= radii[i] <= 10^3`
- `radii` is a 1-D array
