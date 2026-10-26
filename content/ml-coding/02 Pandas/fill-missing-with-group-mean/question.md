---
topic: "Pandas"
difficulty: Medium
---
# Fill Missing Values with the Group Mean

**Topic:** Pandas · **Difficulty:** Medium

## Problem

You get a DataFrame `df` of products with columns `category` and `price`; some prices are missing (`NaN`).

Return a copy of `df` where each missing price is replaced by the mean of the known prices in the same category. If a category has no known prices at all (or the category itself is missing), use the mean of all known prices in `df` instead. If no price is known anywhere, leave the value missing. Keep the original row order and index, and don't modify `df`.

## Examples

**Example 1**
```text
Input: df = {"category": ["a", "a", "b", "a"], "price": [10.0, null, 4.0, 20.0]}
Output: {"category":["a","a","b","a"],"price":[10.00000,15.00000,4.00000,20.00000]}
```

**Example 2**
```text
Input: df = {"category": ["a", "b", "b"], "price": [6.0, null, null]}
Output: {"category":["a","b","b"],"price":[6.00000,6.00000,6.00000]}
Explanation: category b has no known prices, so both use the overall mean 6.0.
```

## Constraints

- `0 <= len(df) <= 10^5`
