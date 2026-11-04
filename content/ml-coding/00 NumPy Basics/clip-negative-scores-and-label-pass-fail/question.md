---
topic: "NumPy Basics"
difficulty: Easy
---
# Clip Negative Scores and Label Pass/Fail

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

A grading script receives a 1-D float array `scores` of shape `(n,)`. Some entries are negative because of data-entry errors. Write a function `clean_and_label(scores, threshold)` that returns a tuple `(clean, labels)`:

- `clean`: a float `np.ndarray` of shape `(n,)` where every negative score is replaced by `0` and all other scores are unchanged.
- `labels`: a Python `list[str]` of length `n`. Entry `i` is `'pass'` if `clean[i] >= threshold`, otherwise `'fail'`. The labels are based on the cleaned scores.

Calls to practise: `np.where` (twice) and `.tolist()` to turn the label array into a plain list. The whole solution should fit in 1-3 lines.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: scores = [-5.0, 55.5, 80.0], threshold = 60.0
Output: ([0.00000,55.50000,80.00000], ["fail","fail","pass"])
Explanation: -5.0 becomes 0.0; only 80.0 reaches the threshold.
```

**Example 2**
```text
Input: scores = [60.0, -1.0, 90.0, 59.5], threshold = 60.0
Output: ([60.00000,0.00000,90.00000,59.50000], ["pass","fail","pass","fail"])
Explanation: a score equal to the threshold passes.
```

**Example 3**
```text
Input: scores = [-3.0], threshold = 0.0
Output: ([0.00000], ["pass"])
Explanation: the cleaned score 0.0 meets the threshold 0.0.
```

## Constraints

- `1 <= n <= 10^3`
- `-100.0 <= scores[i] <= 100.0`
- `-10.0 <= threshold <= 100.0`
