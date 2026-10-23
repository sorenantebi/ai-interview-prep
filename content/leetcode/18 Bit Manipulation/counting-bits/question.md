---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/counting-bits/
neetcode: https://neetcode.io/problems/counting-bits
---
# Counting Bits

**Topic:** Bit Manipulation · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/counting-bits/) · [NeetCode](https://neetcode.io/problems/counting-bits)

## Problem

Given a non-negative integer `n`, return an array `ans` of length `n + 1` where `ans[i]` is the number of `1` bits in the binary representation of `i`, for every `0 <= i <= n`.

Follow-up: can you do it in `O(n)` total time, without a built-in popcount?

## Examples

**Example 1**
```text
Input: n = 2
Output: [0,1,1]
Explanation: 0 -> 0, 1 -> 1, 2 -> 10
```

**Example 2**
```text
Input: n = 5
Output: [0,1,1,2,1,2]
Explanation: 3 -> 11, 4 -> 100, 5 -> 101
```

## Constraints

- `0 <= n <= 10^5`
