---
topic: "Pandas"
difficulty: Easy
---
# Add a Ratio Column

**Topic:** Pandas · **Difficulty:** Easy

## Problem

You get a DataFrame `df` of ad statistics with integer columns `clicks` and `views`.

Return a copy of `df` with one extra column `ctr` (click-through rate) at the end, equal to `clicks / views`. Where `views` is 0 the rate is undefined: put `NaN` there instead of `inf`. Keep the original columns and row order, and don't modify `df`.

## Examples

**Example 1**
```text
Input: df = {"clicks": [3, 0, 5], "views": [10, 4, 0]}
Output: {"clicks":[3,0,5],"views":[10,4,0],"ctr":[0.30000,0.00000,null]}
Explanation: the last row has no views, so its rate is NaN (shown as null).
```

**Example 2**
```text
Input: df = {"clicks": [0, 7], "views": [0, 7]}
Output: {"clicks":[0,7],"views":[0,7],"ctr":[null,1.00000]}
```

## Constraints

- `0 <= len(df) <= 10^5`
- `0 <= clicks <= views` except that `views` may be 0
