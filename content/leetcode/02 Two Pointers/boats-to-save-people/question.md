---
video: https://www.youtube.com/watch?v=XbaxWuHIWUs
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/boats-to-save-people/
neetcode: https://neetcode.io/problems/boats-to-save-people
---
# Boats to Save People

**Topic:** Two Pointers · **Difficulty:** Medium

## Problem

You are given an array `people`, where `people[i]` is the weight of the i-th person, and an unlimited supply of boats. Each boat can carry a total weight of at most `limit`, and at most two people at the same time, as long as the sum of their weights does not exceed `limit`.

Return the minimum number of boats needed to carry every person.

## Examples

**Example 1**
```text
Input: people = [1,2], limit = 3
Output: 1
Explanation: 1 boat (1, 2)
```

**Example 2**
```text
Input: people = [3,2,2,1], limit = 3
Output: 3
Explanation: 3 boats (1, 2), (2) and (3)
```

**Example 3**
```text
Input: people = [3,5,3,4], limit = 5
Output: 4
Explanation: 4 boats (3), (3), (4), (5)
```

## Constraints

- `1 <= people.length <= 5 * 10^4`
- `1 <= people[i] <= limit <= 3 * 10^4`
