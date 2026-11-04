---
topic: "Pandas Basics"
difficulty: Easy
---
# Clean a Survey Table

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

A small survey table arrives with missing values and misspelled labels. Write `clean_table(df, defaults, fixes)` that returns a cleaned copy of the DataFrame.

- `df` is a `pd.DataFrame` with any number of columns (strings, floats or ints).
- `defaults` is a `dict` mapping a column name to the value that should replace missing values (`NaN` / `None`) in that column. Columns that are not in `defaults` keep their missing values.
- `fixes` is a nested `dict` of the form `{column: {old_value: new_value}}`. Every occurrence of `old_value` in that column must be replaced by `new_value`. Columns that are not in `fixes` stay unchanged.

First fill the missing values, then apply the replacements (so a default value can itself be corrected by `fixes`). Return the new DataFrame with the same index and columns as the input.

**Practise these calls:** `DataFrame.fillna` with a dict, and `DataFrame.replace` with a nested dict. No Python loops are needed; the whole solution fits in one to three lines.

## Examples

**Example 1**
```text
Input: df = {"city": ["Berlin", "Bon", null, "Bonn"], "age": [25.0, null, 31.0, null]}, defaults = {"city": "unknown", "age": 30.0}, fixes = {"city": {"Bon": "Bonn"}}
Output: {"city": ["Berlin", "Bonn", "unknown", "Bonn"], "age": [25.00000, 30.00000, 31.00000, 30.00000]}
Explanation: the missing city becomes "unknown", the typo "Bon" becomes "Bonn", and both missing ages become 30.0.
```

**Example 2**
```text
Input: df = {"grade": ["A", "a", "B", null], "score": [1.5, 2.5, null, 4.0]}, defaults = {"grade": "F"}, fixes = {"grade": {"a": "A"}}
Output: {"grade": ["A", "A", "B", "F"], "score": [1.50000, 2.50000, null, 4.00000]}
Explanation: "score" is not in `defaults`, so its missing value stays NaN.
```

## Constraints

- `1 <= len(df) <= 10^3`
- Every key of `defaults` and `fixes` is a column of `df`.
- `defaults` and `fixes` are non-empty.
