---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/car-fleet/
neetcode: https://neetcode.io/problems/car-fleet
---
# Car Fleet

**Topic:** Stack · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/car-fleet/) · [NeetCode](https://neetcode.io/problems/car-fleet)

## Problem

There are `n` cars on a one-lane road heading to a destination at mile `target`. Car `i` starts at mile `position[i]` and drives at constant speed `speed[i]` (miles per hour). All positions are distinct.

A car can never pass the car in front of it. If it catches up, it slows down and drives bumper-to-bumper at the slower car's speed; from then on they move together as one **car fleet**. A single car on its own is also a fleet. If a car catches up with a fleet exactly at the destination, it still counts as part of that fleet.

Return the number of distinct car fleets that arrive at the destination.

## Examples

**Example 1**
```text
Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
Output: 3
Explanation: cars at 10 and 8 meet at 12; car at 0 alone; cars at 5 and 3 meet at 6
```

**Example 2**
```text
Input: target = 10, position = [3], speed = [3]
Output: 1
```

**Example 3**
```text
Input: target = 100, position = [0,2,4], speed = [4,2,1]
Output: 1
```

## Constraints

- `n == position.length == speed.length`
- `1 <= n <= 10^5`
- `0 < target <= 10^6`
- `0 <= position[i] < target`, all positions are unique
- `0 < speed[i] <= 10^6`
