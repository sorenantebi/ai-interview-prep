---
topic: "Pandas"
difficulty: Medium
---
# Pivot a Sales Table

**Topic:** Pandas · **Difficulty:** Medium

## Problem

You get a DataFrame `df` of sales in long format with columns `region`, `month` (a string such as `"2024-01"`) and `amount`. The same region and month can appear in several rows.

Return a wide table with one row per region and one column per month:

- the first column is `region`, rows sorted by region;
- then one column per month that appears anywhere in `df`, in ascending order, named by the month string;
- each cell is the total `amount` for that region and month, or `0` when there were no sales.

Use a default `0..n-1` index.

## Examples

**Example 1**
```text
Input: df = {"region": ["east", "west", "east", "east"], "month": ["2024-02", "2024-01", "2024-01", "2024-02"], "amount": [5.0, 3.0, 2.0, 1.0]}
Output: {"region":["east","west"],"2024-01":[2.00000,3.00000],"2024-02":[6.00000,0.00000]}
Explanation: east sold 2 in January and 5 + 1 in February; west sold nothing in February.
```

**Example 2**
```text
Input: df = {"region": ["north"], "month": ["2023-12"], "amount": [9.5]}
Output: {"region":["north"],"2023-12":[9.50000]}
```

## Constraints

- `1 <= len(df) <= 10^5`
- `amount >= 0`
