---
topic: "Pandas Basics"
difficulty: Easy
---
# Filter Rows with Several Conditions

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

You are given a `pd.DataFrame` `df` with the columns `name` (str), `type` (str), `level` (int) and `featured` (bool), a list of strings `types`, and an integer `k`.

Return a new DataFrame that keeps only the rows where **both** of these hold:

- `type` is one of the values in `types`
- `level` is greater than `k` **or** `featured` is `True`

The kept rows must stay in their original order, all four columns must be kept, and the returned DataFrame must have a fresh index `0, 1, 2, ...`. If no row matches, return an empty DataFrame with the same columns.

This is a fundamentals drill. Practise these calls: boolean masks combined with `&` and `|` (put each comparison in parentheses), `Series.isin`, selecting rows with `df[mask]`, and `reset_index(drop=True)`. The solution fits in 1-3 lines, so don't write a loop over the rows.

## Examples

**Example 1**
```text
Input: df = {"name": ["a", "b", "c", "d"], "type": ["tool", "gem", "tool", "food"], "level": [5, 2, 1, 9], "featured": [false, false, true, false]}, types = ["tool", "gem"], k = 2
Output: {"name": ["a", "c"], "type": ["tool", "tool"], "level": [5, 1], "featured": [false, true]}
Explanation: "a" has level 5 > 2. "b" has level 2, which is not above 2, and is not featured. "c" has level 1 but is featured. "d" has a type that is not in the list.
```

**Example 2**
```text
Input: df = {"name": ["x"], "type": ["tool"], "level": [7], "featured": [true]}, types = ["food"], k = 0
Output: {"name": [], "type": [], "level": [], "featured": []}
Explanation: The only row has a type that is not in the list, so nothing is kept.
```

## Constraints

- `0 <= len(df) <= 10^4`
- `types` may be empty
- `level` values and `k` are integers
