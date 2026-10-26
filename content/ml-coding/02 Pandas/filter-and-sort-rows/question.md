---
topic: "Pandas"
difficulty: Easy
---
# Filter and Sort Rows

**Topic:** Pandas · **Difficulty:** Easy

## Problem

You get a DataFrame `df` with columns `name` (string) and `score` (number), and a threshold `min_score`.

Return a new DataFrame with only the rows whose `score` is at least `min_score`, sorted by `score` from highest to lowest. Rows with the same score are ordered by `name` alphabetically. Keep both columns in the same order and return the result with a default `0..n-1` index. Don't modify `df`.

## Examples

**Example 1**
```text
Input: df = {"name": ["ana", "ben", "cy", "dee"], "score": [72, 90, 65, 90]}, min_score = 70
Output: {"name":["ben","dee","ana"],"score":[90,90,72]}
Explanation: cy is dropped; ben and dee tie on 90 and are ordered by name.
```

**Example 2**
```text
Input: df = {"name": ["zed", "amy"], "score": [50, 40]}, min_score = 60
Output: {"name":[],"score":[]}
```

## Constraints

- `0 <= len(df) <= 10^5`
- names are unique
