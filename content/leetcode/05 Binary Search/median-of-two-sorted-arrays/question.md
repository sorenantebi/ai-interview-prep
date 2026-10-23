---
topic: "Binary Search"
difficulty: Hard
leetcode: https://leetcode.com/problems/median-of-two-sorted-arrays/
neetcode: https://neetcode.io/problems/median-of-two-sorted-arrays
---
# Median of Two Sorted Arrays

**Topic:** Binary Search · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/median-of-two-sorted-arrays/) · [NeetCode](https://neetcode.io/problems/median-of-two-sorted-arrays)

## Problem

Given two sorted arrays `nums1` (length `m`) and `nums2` (length `n`), return the median of the combined collection of all `m + n` numbers. If the total count is even, the median is the average of the two middle values. The overall run time should be `O(log(m + n))`.

## Examples

**Example 1**
```text
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged = [1,2,3]
```

**Example 2**
```text
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged = [1,2,3,4], (2 + 3) / 2 = 2.5
```

**Example 3**
```text
Input: nums1 = [], nums2 = [1]
Output: 1.00000
```

## Constraints

- `0 <= m, n <= 1000`
- `1 <= m + n <= 2000`
- `-10^6 <= nums1[i], nums2[i] <= 10^6`
- Both arrays are sorted in non-decreasing order
