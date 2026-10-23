---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/gas-station/
neetcode: https://neetcode.io/problems/gas-station
---
# Gas Station - Solution

**Question:** Gas Station - Question · **Difficulty:** Medium

## Intuition

If total gas `<` total cost, no start works. Otherwise a solution exists, and we can find it greedily: drive from a candidate start keeping a running tank; if the tank goes negative at station `i`, **no** station between the candidate and `i` can be a valid start (each would arrive at `i` with even less fuel), so jump the candidate to `i + 1`.

## Approach

1. If `sum(gas) < sum(cost)`, return `-1`.
2. `tank = 0`, `start = 0`.
3. For each `i`: `tank += gas[i] - cost[i]`; if `tank < 0`, set `start = i + 1` and `tank = 0`.
4. Return `start`.

## Code

```python
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        start, end = len(gas) - 1, 0
        total = gas[start] - cost[start]

        while start >= end:
            while total < 0 and start >= end:
                start -= 1
                total += gas[start] - cost[start]
            if start == end:
                return start
            total += gas[end] - cost[end]
            end += 1
        return -1
```

## Complexity

- **Time:** `O(n)` — one pass (plus the two sums).
- **Space:** `O(1)` — constant extra state.

## Other Approaches

- **Brute force simulation:** try every start and simulate the loop — Time `O(n^2)`, Space `O(1)`.
- **Minimum prefix sum:** the start is the index right after the minimum prefix of `gas[i] - cost[i]` — Time `O(n)`, Space `O(1)`.

## Key Takeaway

When a running balance fails at `i`, every start in the failed segment fails too — so skip past the whole segment; a global feasibility check (`total >= 0`) guarantees the surviving candidate works.
