---
topic: "Pandas Basics"
difficulty: Easy
---
# Scores Above a Threshold

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

This is a fundamentals drill on `pd.Series`. Write a function `above_threshold(scores, threshold)` that receives a dict `scores` mapping string labels to float values, and a float `threshold`.

Build a `pd.Series` from the dict (the keys become the index), then return a new `pd.Series` containing only the entries whose value is **strictly greater** than `threshold`. The labels must stay as the index, and the original order is kept.

Calls to practise:
- `pd.Series(dict)` to build a Series with the keys as its index
- a boolean mask such as `s > threshold`
- label-based selection with `.loc[...]`

If no entry is above the threshold, return an empty Series.

## Examples

**Example 1**
```text
Input: scores = {"a": 1.0, "b": 3.5, "c": 2.0, "d": 5.0}, threshold = 2.0
Output: {"b":3.50000,"d":5.00000}
Explanation: "c" equals the threshold, so it is not strictly above it.
```

**Example 2**
```text
Input: scores = {"x": 0.5, "y": 0.25}, threshold = 1.0
Output: {}
Explanation: No value is above 1.0, so the result is an empty Series.
```

**Example 3**
```text
Input: scores = {"mon": 10.0, "tue": 12.5, "wed": 9.0}, threshold = 9.5
Output: {"mon":10.00000,"tue":12.50000}
```

## Constraints

- `1 <= len(scores) <= 10^4`
- Keys are unique strings; values are finite floats.
