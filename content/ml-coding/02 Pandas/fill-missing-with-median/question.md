---
topic: "Pandas"
difficulty: Easy
---
# Fill Missing Values with the Median

**Topic:** Pandas · **Difficulty:** Easy

## Problem

You get a DataFrame `df` with some missing values (`NaN`).

Return a new DataFrame where every missing value in a numeric column is replaced by that column's median (computed from the values that are present). Non-numeric columns stay exactly as they are, missing values included. A numeric column with no values at all stays all `NaN`. Keep columns and rows in the same order and don't modify `df`.

## Examples

**Example 1**
```text
Input: df = {"age": [30, null, 50, 20], "city": ["a", null, "b", "c"]}
Output: {"age":[30.00000,30.00000,50.00000,20.00000],"city":["a",null,"b","c"]}
Explanation: the median of 30, 50 and 20 is 30; the missing city stays missing.
```

**Example 2**
```text
Input: df = {"x": [1.0, 2.0, null], "y": [null, null, 4.0]}
Output: {"x":[1.00000,2.00000,1.50000],"y":[4.00000,4.00000,4.00000]}
```

## Constraints

- `0 <= len(df) <= 10^5`
- `1 <= number of columns <= 50`
