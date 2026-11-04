---
topic: "Segment Tree"
difficulty: Medium
leetcode: https://leetcode.com/problems/range-sum-query-mutable/
---
# Range Sum Query - Mutable

**Topic:** Segment Tree · **Difficulty:** Medium

## Problem

Design a data structure that stores an integer array `nums` and supports two operations: changing the value at a given position, and computing the sum of a contiguous range of elements.

Implement the `NumArray` class:

- `NumArray(int[] nums)` initializes the object with the integer array `nums`.
- `void update(int index, int val)` sets `nums[index]` to `val`.
- `int sumRange(int left, int right)` returns the sum of the elements of `nums` between indices `left` and `right` inclusive, i.e. `nums[left] + nums[left + 1] + ... + nums[right]`.

## Examples

**Example 1**
```text
Input
["NumArray", "sumRange", "update", "sumRange"]
[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
Output
[null, 9, null, 8]
```

Explanation:
```text
NumArray numArray = new NumArray([1, 3, 5]);
numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
numArray.update(1, 2);   // nums = [1, 2, 5]
numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8
```

## Constraints

- `1 <= nums.length <= 3 * 10^4`
- `-100 <= nums[i] <= 100`
- `0 <= index < nums.length`
- `-100 <= val <= 100`
- `0 <= left <= right < nums.length`
- At most `3 * 10^4` calls will be made to `update` and `sumRange`.
