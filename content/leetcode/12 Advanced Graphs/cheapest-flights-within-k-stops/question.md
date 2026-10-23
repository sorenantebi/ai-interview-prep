---
topic: "Advanced Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/cheapest-flights-within-k-stops/
neetcode: https://neetcode.io/problems/cheapest-flight-path
---
# Cheapest Flights Within K Stops

**Topic:** Advanced Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/cheapest-flights-within-k-stops/) · [NeetCode](https://neetcode.io/problems/cheapest-flight-path)

## Problem

There are `n` cities numbered `0` to `n - 1`, connected by directed flights. `flights[i] = [from_i, to_i, price_i]` is a flight from `from_i` to `to_i` costing `price_i`.

Given `src`, `dst`, and an integer `k`, return the cheapest total price to fly from `src` to `dst` using **at most `k` stops** (i.e. at most `k + 1` flights; intermediate cities count as stops). If no such route exists, return `-1`.

## Examples

**Example 1**
```text
Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1
Output: 700
Explanation: 0 -> 1 -> 3 costs 700. 0 -> 1 -> 2 -> 3 is cheaper (400) but uses 2 stops.
```

**Example 2**
```text
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
Output: 200
```

**Example 3**
```text
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
Output: 500
```

## Constraints

- `1 <= n <= 100`
- `0 <= flights.length <= n * (n - 1) / 2`
- `flights[i].length == 3`, `0 <= from_i, to_i < n`, `from_i != to_i`
- `1 <= price_i <= 10^4`
- No duplicate flights between the same ordered pair.
- `0 <= src, dst, k < n`, `src != dst`
