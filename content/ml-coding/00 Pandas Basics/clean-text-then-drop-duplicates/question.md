---
topic: "Pandas Basics"
difficulty: Easy
---
# Clean Text, Then Drop Duplicates

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

A visitor log has been typed in by hand, so the same city shows up as `" Berlin"`, `"berlin "` and `"BERLIN"`. Write `clean_and_dedupe(df)`, which receives a `pd.DataFrame` with a text column `"city"` and one or more other columns (e.g. `"visitors"`), and returns a cleaned DataFrame.

Do it in this order:

1. Standardise the `"city"` column: remove leading/trailing whitespace and convert to lowercase.
2. Drop duplicate rows (rows that are equal in **all** columns), keeping the first occurrence.

The surviving rows keep their original order and their original index labels (do not reset the index). The input DataFrame should not be modified.

**Calls to practise:** `Series.str.strip()`, `Series.str.lower()`, `DataFrame.assign` (or column assignment on a copy) and `DataFrame.drop_duplicates(keep="first")`. The intended solution is 1-3 lines, with no Python loops.

## Examples

**Example 1**
```text
Input: df = {"city": [" Berlin", "berlin ", "Bonn"], "visitors": [10, 10, 7]}
Output: {"city": ["berlin", "bonn"], "visitors": [10, 7]}
Explanation: After cleaning, rows 0 and 1 are identical, so row 1 is dropped. The result has index labels 0 and 2.
```

**Example 2**
```text
Input: df = {"city": ["Ulm ", " ULM"], "visitors": [5, 6]}
Output: {"city": ["ulm", "ulm"], "visitors": [5, 6]}
Explanation: The cities match after cleaning, but the visitor counts differ, so both rows are kept.
```

**Example 3**
```text
Input: df = {"city": ["HAMBURG", "Hamburg", "hamburg ", " Hamburg"], "visitors": [3, 3, 3, 3]}
Output: {"city": ["hamburg"], "visitors": [3]}
Explanation: All four rows are the same after cleaning; only the first (index 0) is kept.
```

## Constraints

- `1 <= len(df) <= 10^4`
- `"city"` contains non-missing strings only.
- Duplicates are judged on all columns, after the `"city"` column has been cleaned.
