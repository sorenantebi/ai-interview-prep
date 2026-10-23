---
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/happy-number/
neetcode: https://neetcode.io/problems/non-cyclical-number
---
# Happy Number

**Topic:** Math & Geometry · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/happy-number/) · [NeetCode](https://neetcode.io/problems/non-cyclical-number)

## Problem

Determine whether a positive integer `n` is **happy**.

Repeatedly replace the number with the sum of the squares of its digits. If this process eventually reaches `1`, the number is happy and you return `true`. Otherwise the process loops forever in a cycle that never contains `1`, and you return `false`.

## Examples

**Example 1**
```text
Input: n = 19
Output: true
Explanation: 1^2 + 9^2 = 82 -> 8^2 + 2^2 = 68 -> 6^2 + 8^2 = 100 -> 1^2 + 0^2 + 0^2 = 1
```

**Example 2**
```text
Input: n = 2
Output: false
Explanation: 2 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4 -> ... (cycle without 1)
```

## Constraints

- `1 <= n <= 2^31 - 1`
