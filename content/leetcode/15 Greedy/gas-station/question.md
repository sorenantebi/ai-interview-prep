---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/gas-station/
neetcode: https://neetcode.io/problems/gas-station
---
# Gas Station

**Topic:** Greedy · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/gas-station/) · [NeetCode](https://neetcode.io/problems/gas-station)

## Problem

There are `n` gas stations on a circular route. Station `i` provides `gas[i]` units of fuel, and driving from station `i` to station `i + 1` (wrapping to 0 after the last) costs `cost[i]` units. Your car has an unlimited tank and starts **empty** at a station of your choice.

Return the index of the starting station from which you can travel around the full circuit once in the clockwise direction, or `-1` if no such station exists. If a solution exists it is guaranteed to be **unique**.

## Examples

**Example 1**
```text
Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
Output: 3
```

**Example 2**
```text
Input: gas = [2,3,4], cost = [3,4,3]
Output: -1
Explanation: Total gas 9 < total cost 10.
```

## Constraints

- `n == gas.length == cost.length`
- `1 <= n <= 10^5`
- `0 <= gas[i], cost[i] <= 10^4`
