---
topic: "Pandas"
difficulty: Medium
---
# Rolling 7-Day Average

**Topic:** Pandas · **Difficulty:** Medium

## Problem

You get a DataFrame `df` of daily sales with columns `date` (an ISO string `"YYYY-MM-DD"`) and `sales`. Each date appears at most once, but the rows aren't sorted and some days are missing.

Return a DataFrame sorted by date with columns `date` (the original strings), `sales` and `avg_7d`. `avg_7d` is the mean of `sales` over the 7 calendar days ending on that row's date, both ends included (that date and the 6 days before it). Only days present in `df` count: a missing day is skipped, not treated as 0. Use a default `0..n-1` index.

## Examples

**Example 1**
```text
Input: df = {"date": ["2024-01-03", "2024-01-01", "2024-01-02"], "sales": [30.0, 10.0, 20.0]}
Output: {"date":["2024-01-01","2024-01-02","2024-01-03"],"sales":[10.00000,20.00000,30.00000],"avg_7d":[10.00000,15.00000,20.00000]}
```

**Example 2**
```text
Input: df = {"date": ["2024-01-01", "2024-01-07", "2024-01-08"], "sales": [7.0, 1.0, 4.0]}
Output: {"date":["2024-01-01","2024-01-07","2024-01-08"],"sales":[7.00000,1.00000,4.00000],"avg_7d":[7.00000,4.00000,2.50000]}
Explanation: the window for Jan 8 is Jan 2–8, so Jan 1 has dropped out: (1 + 4) / 2 = 2.5.
```

## Constraints

- `1 <= len(df) <= 10^5`
- dates are unique
