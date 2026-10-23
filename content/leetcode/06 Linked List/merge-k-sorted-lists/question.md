---
topic: "Linked List"
difficulty: Hard
leetcode: https://leetcode.com/problems/merge-k-sorted-lists/
neetcode: https://neetcode.io/problems/merge-k-sorted-linked-lists
---
# Merge K Sorted Lists

**Topic:** Linked List · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/merge-k-sorted-lists/) · [NeetCode](https://neetcode.io/problems/merge-k-sorted-linked-lists)

## Problem

You are given an array `lists` of `k` linked lists, each sorted in ascending order. Merge them all into a single sorted linked list and return its head. `lists` may be empty, and individual lists may be empty.

## Examples

**Example 1**
```text
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
```

**Example 2**
```text
Input: lists = []
Output: []
```

**Example 3**
```text
Input: lists = [[]]
Output: []
```

## Constraints

- `k == lists.length`, `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- Each `lists[i]` is sorted in ascending order
- The total number of nodes does not exceed `10^4`
