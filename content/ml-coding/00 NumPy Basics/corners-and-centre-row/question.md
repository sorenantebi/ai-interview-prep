---
topic: "NumPy Basics"
difficulty: Easy
---
# Corners and Centre Row

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

This is a fundamentals drill on indexing a 2-D array. Practise these calls: `a[i, j]`, negative indices such as `a[-1, -1]`, and `a[i]` for a whole row.

Write `corners_and_centre(a)`, which receives a 2-D float array `a` of shape `(n, m)` and returns a tuple `(corners, centre)`:

- `corners`: a 1-D array of length 4 with the four corner elements in the order top-left, top-right, bottom-left, bottom-right, i.e. `a[0, 0]`, `a[0, -1]`, `a[-1, 0]`, `a[-1, -1]`.
- `centre`: the centre row, `a[n // 2]`, as a 1-D array of length `m`. For an even `n` this is the lower of the two middle rows.

If `n` or `m` is 1, the corners simply repeat (they are still four values).

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: a = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
Output: ([1.00000,3.00000,7.00000,9.00000],[4.00000,5.00000,6.00000])
Explanation: n = 3, so the centre row is a[1].
```

**Example 2**
```text
Input: a = [[5.0]]
Output: ([5.00000,5.00000,5.00000,5.00000],[5.00000])
Explanation: With a single element, all four corners are that element.
```

**Example 3**
```text
Input: a = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]]
Output: ([1.00000,2.00000,7.00000,8.00000],[5.00000,6.00000])
Explanation: n = 4, so the centre row is a[4 // 2] = a[2].
```

## Constraints

- `a` is a 2-D `float64` array
- `1 <= n, m <= 100`
