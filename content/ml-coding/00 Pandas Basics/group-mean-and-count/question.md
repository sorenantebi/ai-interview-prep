---
topic: "Pandas Basics"
difficulty: Easy
---
# Group Mean and Count

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

You receive a `pd.DataFrame` `df` and two column names, `key` and `value`. The `key` column holds a group label (strings or integers) and the `value` column holds floats.

Return a new `pd.DataFrame` with one row per distinct label in `key`. The index is the group label (named `key`, sorted ascending) and there are exactly two columns, in this order:

- `"mean"`: the mean of `value` within the group
- `"count"`: the number of rows in the group

Calls to practise: `df.groupby(...)`, `.mean()` and `.size()`. Don't use Python loops over the rows or groups.

## Examples

**Example 1**
```text
Input: df = {"team": ["a", "b", "a", "b", "a"], "score": [1.0, 2.0, 3.0, 6.0, 5.0]}, key = "team", value = "score"
Output: {"mean":{"a":3.00000,"b":4.00000},"count":{"a":3,"b":2}}
Explanation: team a has scores 1, 3, 5 (mean 3, 3 rows); team b has 2, 6 (mean 4, 2 rows).
```

**Example 2**
```text
Input: df = {"city": ["x", "x"], "price": [10.0, 20.0]}, key = "city", value = "price"
Output: {"mean":{"x":15.00000},"count":{"x":2}}
```

**Example 3**
```text
Input: df = {"city": ["b", "a", "b"], "v": [2.0, 4.0, 6.0]}, key = "city", value = "v"
Output: {"mean":{"a":4.00000,"b":4.00000},"count":{"a":1,"b":2}}
Explanation: the groups appear sorted by label, not in order of first appearance.
```

## Constraints

- `1 <= len(df) <= 10^5`
- `key` and `value` are columns of `df`; `value` contains no NaN
- `df` may contain other columns, which are ignored
