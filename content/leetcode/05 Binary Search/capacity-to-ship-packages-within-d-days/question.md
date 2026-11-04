---
video: https://www.youtube.com/watch?v=ER_oLmdc-nw
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/
neetcode: https://neetcode.io/problems/capacity-to-ship-packages-within-d-days
---
# Capacity To Ship Packages Within D Days

**Topic:** Binary Search · **Difficulty:** Medium

## Problem

A conveyor belt carries packages that must be shipped from one port to another within `days` days.

The `i`-th package has weight `weights[i]`. Each day, the ship is loaded with packages from the belt in the given order, and the total loaded weight may not exceed the ship's maximum weight capacity.

Return the least weight capacity of the ship that allows all packages to be shipped within `days` days.

## Examples

**Example 1**
```text
Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
```
A capacity of 15 is the minimum that works: day 1 ships 1, 2, 3, 4, 5; day 2 ships 6, 7; day 3 ships 8; day 4 ships 9; day 5 ships 10. Packages must be shipped in order, so regrouping such as (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) with capacity 14 is not allowed.

**Example 2**
```text
Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
```
Day 1 ships 3, 2; day 2 ships 2, 4; day 3 ships 1, 4.

**Example 3**
```text
Input: weights = [1,2,3,1,1], days = 4
Output: 3
```
Day 1 ships 1; day 2 ships 2; day 3 ships 3; day 4 ships 1, 1.

## Constraints

- `1 <= days <= weights.length <= 5 * 10^4`
- `1 <= weights[i] <= 500`
