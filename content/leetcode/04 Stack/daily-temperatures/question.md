---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/daily-temperatures/
neetcode: https://neetcode.io/problems/daily-temperatures
---
# Daily Temperatures

**Topic:** Stack · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/daily-temperatures/) · [NeetCode](https://neetcode.io/problems/daily-temperatures)

## Problem

Given an integer array `temperatures` of daily temperatures, return an array `answer` where `answer[i]` is the number of days you must wait after day `i` to get a strictly warmer temperature. If no future day is warmer, `answer[i] = 0`.

## Examples

**Example 1**
```text
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
```

**Example 2**
```text
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]
```

**Example 3**
```text
Input: temperatures = [30,60,90]
Output: [1,1,0]
```

## Constraints

- `1 <= temperatures.length <= 10^5`
- `30 <= temperatures[i] <= 100`
