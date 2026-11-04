---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/create-sorted-array-through-instructions/
---
# Create Sorted Array through Instructions

**Topic:** Segment Tree · **Difficulty:** Hard

## Problem

You are given an integer array `instructions`. Starting with an empty container `nums`, process the elements of `instructions` from left to right and insert each one into `nums` so that `nums` stays sorted.

The cost of inserting `instructions[i]` is the minimum of:

- the number of elements currently in `nums` that are strictly less than `instructions[i]`, and
- the number of elements currently in `nums` that are strictly greater than `instructions[i]`.

For example, inserting `3` into `nums = [1,2,3,5]` costs `min(2, 1) = 1`, and `nums` becomes `[1,2,3,3,5]`.

Return the total cost of inserting all elements. Since the answer may be large, return it modulo `10^9 + 7`.

## Examples

**Example 1**
```text
Input: instructions = [1,5,6,2]
Output: 1
```
Inserting 1, 5 and 6 each costs 0. Inserting 2 into `[1,5,6]` costs `min(1, 2) = 1`. Total cost is 1.

**Example 2**
```text
Input: instructions = [1,2,3,6,5,4]
Output: 3
```
Inserting 5 costs `min(3, 1) = 1` and inserting 4 costs `min(3, 2) = 2`; all other insertions cost 0. Total cost is 3.

**Example 3**
```text
Input: instructions = [1,3,3,3,2,4,2,1,2]
Output: 4
```
The non-zero costs are 1 (insert 2), 1 (insert 2) and 2 (insert 2). Total cost is 4.

## Constraints

- `1 <= instructions.length <= 10^5`
- `1 <= instructions[i] <= 10^5`
