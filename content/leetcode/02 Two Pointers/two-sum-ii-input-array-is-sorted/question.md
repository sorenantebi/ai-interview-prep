---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
neetcode: https://neetcode.io/problems/two-integer-sum-ii
---
# Two Sum II Input Array Is Sorted

**Topic:** Two Pointers · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · [NeetCode](https://neetcode.io/problems/two-integer-sum-ii)

## Problem

You are given a **1-indexed** integer array `numbers` sorted in non-decreasing order and an integer `target`. Find the two distinct positions `index1 < index2` whose values add up to `target`, and return them as `[index1, index2]` (both 1-based). Exactly one valid answer is guaranteed, and you may not use the same element twice. The solution must use only constant extra space.

## Examples

**Example 1**
```text
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: 2 + 7 == 9
```

**Example 2**
```text
Input: numbers = [2,3,4], target = 6
Output: [1,3]
```

**Example 3**
```text
Input: numbers = [-1,0], target = -1
Output: [1,2]
```

## Constraints

- `2 <= numbers.length <= 3 * 10^4`
- `-1000 <= numbers[i] <= 1000`, sorted non-decreasing
- `-1000 <= target <= 1000`
- Exactly one solution exists
