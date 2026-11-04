---
topic: "NumPy Basics"
difficulty: Easy
---
# Even Numbers Above a Threshold

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

Write a function `filter_even_above(x, k)` that receives a 1-D integer array `x` (`np.ndarray`, dtype `int`) and an integer `k`. It must return a new 1-D array containing only the elements of `x` that are **even AND strictly greater than `k`**, in their original order.

This is a fundamentals drill. Practise these calls:

- `x % 2 == 0` to build a boolean mask for even numbers
- `x > k` to build a boolean mask for the threshold
- `&` to combine two masks (use parentheses around each comparison; `|` works the same way for "or")
- boolean indexing `x[mask]` to select the elements

The intended solution is one to three lines and needs no Python loops. If no element qualifies, return an empty array.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [1, 2, 3, 4, 5, 6, 7, 8], k = 3
Output: [4, 6, 8]
Explanation: The even elements are 2, 4, 6, 8; of these, 4, 6 and 8 are greater than 3.
```

**Example 2**
```text
Input: x = [-4, -2, 0, 5, 10], k = -3
Output: [-2, 0, 10]
Explanation: -4 is even but not greater than -3. 5 is greater than -3 but odd.
```

**Example 3**
```text
Input: x = [1, 3, 5], k = 0
Output: []
Explanation: No element is even, so the result is empty.
```

## Constraints

- `0 <= len(x) <= 10^5`
- `-10^9 <= x[i], k <= 10^9`
