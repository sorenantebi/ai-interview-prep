---
topic: "Linked List"
difficulty: Easy
leetcode: https://leetcode.com/problems/merge-two-sorted-lists/
neetcode: https://neetcode.io/problems/merge-two-sorted-linked-lists
---
# Merge Two Sorted Lists

**Topic:** Linked List · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/merge-two-sorted-lists/) · [NeetCode](https://neetcode.io/problems/merge-two-sorted-linked-lists)

## Problem

You are given the heads of two singly linked lists, `list1` and `list2`, each already sorted in non-decreasing order. Combine them into one sorted linked list by re-linking (splicing) the existing nodes, and return the head of the merged list. Either input may be empty.

## Examples

**Example 1**
```text
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

**Example 2**
```text
Input: list1 = [], list2 = []
Output: []
```

**Example 3**
```text
Input: list1 = [], list2 = [0]
Output: [0]
```

## Constraints

- The number of nodes in each list is in the range `[0, 50]`
- `-100 <= Node.val <= 100`
- Both lists are sorted in non-decreasing order
