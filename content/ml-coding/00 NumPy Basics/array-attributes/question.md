---
topic: "NumPy Basics"
difficulty: Easy
---
# Array Attributes

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

Every NumPy array carries a few basic facts about itself. Knowing them is the first step in debugging shape and dtype errors.

Write a function `array_info(x)` that receives a NumPy array `x` (any shape, any dtype) and returns a tuple of four values:

1. the number of dimensions, as an `int`
2. the shape, as a `tuple` of `int`
3. the total number of elements, as an `int`
4. the name of the dtype, as a `str` (for example `"float64"`, not `dtype('float64')`)

Calls to practise: `x.ndim`, `x.shape`, `x.size` and `x.dtype` (hint: the dtype object has a `.name` attribute). The whole solution is one `return` statement.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: x = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
Output: (2, (2, 3), 6, "float64")
Explanation: a 2x3 array of Python floats becomes float64.
```

**Example 2**
```text
Input: x = [1, 2, 3, 4]
Output: (1, (4,), 4, "int64")
Explanation: the shape of a 1-D array is a one-element tuple. Assumes a 64-bit platform where integers default to int64.
```

**Example 3**
```text
Input: x = [[[True, False]], [[False, True]]]
Output: (3, (2, 1, 2), 4, "bool")
```

## Constraints

- `x` is a NumPy array with `0 <= ndim <= 4`
- `x` may be empty (some dimension can be 0)
- `x` can have any numeric or boolean dtype
