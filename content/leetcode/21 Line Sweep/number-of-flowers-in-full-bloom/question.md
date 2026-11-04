---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/number-of-flowers-in-full-bloom/
---
# Number of Flowers in Full Bloom

**Topic:** Line Sweep · **Difficulty:** Hard

## Problem

You are given a 0-indexed 2D integer array `flowers`, where `flowers[i] = [start_i, end_i]` means the `i`-th flower is in full bloom from time `start_i` to time `end_i` (both inclusive). You are also given a 0-indexed integer array `people` of size `n`, where `people[i]` is the time the `i`-th person arrives to see the flowers.

Return an integer array `answer` of size `n`, where `answer[i]` is the number of flowers in full bloom when the `i`-th person arrives.

## Examples

**Example 1**
```text
Input: flowers = [[1,6],[3,7],[9,12],[4,13]], people = [2,3,7,11]
Output: [1,2,2,2]
```

**Example 2**
```text
Input: flowers = [[1,10],[3,3]], people = [3,3,2]
Output: [2,2,1]
```

## Constraints

- `1 <= flowers.length <= 5 * 10^4`
- `flowers[i].length == 2`
- `1 <= start_i <= end_i <= 10^9`
- `1 <= people.length <= 5 * 10^4`
- `1 <= people[i] <= 10^9`
