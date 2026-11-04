---
video: https://www.youtube.com/watch?v=RF_M9tX4Eag
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/reverse-linked-list-ii/
neetcode: https://neetcode.io/problems/reverse-linked-list-ii
---
# Reverse Linked List II

**Topic:** Linked List · **Difficulty:** Medium

## Problem

You are given the head of a singly linked list and two integers `left` and `right` with `left <= right`. Positions are 1-indexed. Reverse the nodes of the list from position `left` to position `right`, and return the head of the resulting list.

Follow up: can you do it in one pass?

## Examples

**Example 1**
```text
Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]
```

**Example 2**
```text
Input: head = [5], left = 1, right = 1
Output: [5]
```

## Constraints

- The number of nodes in the list is `n`.
- `1 <= n <= 500`
- `-500 <= Node.val <= 500`
- `1 <= left <= right <= n`
