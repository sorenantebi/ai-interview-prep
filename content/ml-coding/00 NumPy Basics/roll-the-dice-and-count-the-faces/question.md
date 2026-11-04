---
topic: "NumPy Basics"
difficulty: Easy
---
# Roll the Dice and Count the Faces

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

Write a function `roll_dice(n, seed)` that simulates `n` rolls of a fair six-sided die and counts how often each face came up.

- Create a random generator with `np.random.default_rng(seed)`.
- Draw the rolls with `rng.integers(1, 7, size=n)`. This gives a 1-D integer array of length `n` with values in `1..6`. Draw exactly once, so the result matches the tests for a given seed.
- Count the faces with `np.bincount`. Use its `minlength` argument so that faces that never appear still get a count of `0`.

Return a tuple `(rolls, counts)`:

- `rolls`: 1-D integer array of shape `(n,)`, the dice rolls in the order they were drawn.
- `counts`: 1-D integer array of shape `(6,)`, where `counts[i]` is the number of rolls showing face `i + 1`. Always `counts.sum() == n`.

Calls to practise: `np.random.default_rng`, `Generator.integers`, `np.bincount` (with `minlength`) and slicing.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: n = 0, seed = 0
Output: ([], [0,0,0,0,0,0])
Explanation: No dice are rolled, so every face has count 0.
```

**Example 2**
```text
Input: n = 0, seed = 5
Output: ([], [0,0,0,0,0,0])
Explanation: The counts array still has 6 entries (minlength), regardless of the seed.
```

## Constraints

- `0 <= n <= 10^5`
- `seed` is a non-negative integer
