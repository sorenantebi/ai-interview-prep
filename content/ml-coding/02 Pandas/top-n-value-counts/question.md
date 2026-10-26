---
topic: "Pandas"
difficulty: Easy
---
# Top N Value Counts

**Topic:** Pandas · **Difficulty:** Easy

## Problem

You get a Series `s` of category labels (strings, possibly with missing values) and an integer `n`.

Return a Series with the `n` most frequent labels and how often each occurs: the index is the label and the values are the counts. Order it by count from highest to lowest; labels with the same count are ordered alphabetically. Missing values are not counted. If there are fewer than `n` distinct labels, return all of them.

## Examples

**Example 1**
```text
Input: s = ["cat", "dog", "cat", "bird", "dog", "cat"], n = 2
Output: {"cat":3,"dog":2}
```

**Example 2**
```text
Input: s = ["b", "a", null, "c", "a", "b"], n = 5
Output: {"a":2,"b":2,"c":1}
Explanation: a and b tie on 2 and are ordered alphabetically; the missing value is ignored.
```

## Constraints

- `0 <= len(s) <= 10^5`
- `1 <= n <= 10^5`
