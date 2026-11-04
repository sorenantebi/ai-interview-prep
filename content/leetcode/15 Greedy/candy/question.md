---
video: https://www.youtube.com/watch?v=1IzCRCcK17A
topic: "Greedy"
difficulty: Hard
leetcode: https://leetcode.com/problems/candy/
neetcode: https://neetcode.io/problems/candy
---
# Candy

**Topic:** Greedy · **Difficulty:** Hard

## Problem

There are `n` children standing in a line. Each child has a rating value given in the integer array `ratings`.

You must give candies to the children so that:

- Each child gets at least one candy.
- A child with a higher rating than a neighbor gets more candies than that neighbor.

Return the minimum number of candies needed to distribute to the children.

## Examples

**Example 1**
```text
Input: ratings = [1,0,2]
Output: 5
Explanation: Give the first, second and third child 2, 1, 2 candies respectively.
```

**Example 2**
```text
Input: ratings = [1,2,2]
Output: 4
Explanation: Give the first, second and third child 1, 2, 1 candies respectively.
The third child gets 1 candy because it satisfies both conditions (a neighbor with an equal rating does not force more candies).
```

## Constraints

- `1 <= n == ratings.length <= 5 * 10^4`
- `0 <= ratings[i] <= 5 * 10^4`
