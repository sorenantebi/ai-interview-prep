---
topic: "Linked List"
difficulty: Easy
leetcode: https://leetcode.com/problems/reverse-linked-list/
neetcode: https://neetcode.io/problems/reverse-a-linked-list
---
# Reverse Linked List

**Topic:** Linked List · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/reverse-linked-list/) · [NeetCode](https://neetcode.io/problems/reverse-a-linked-list)

## Problem

You are given the `head` of a singly linked list. Reverse the list so that every `next` pointer points to the previous node instead of the following one, and return the head of the reversed list (the original tail). An empty list stays empty.

## Examples

**Example 1**
```text
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
```

**Example 2**
```text
Input: head = [1,2]
Output: [2,1]
```

**Example 3**
```text
Input: head = []
Output: []
```

## Constraints

- The number of nodes is in the range `[0, 5000]`
- `-5000 <= Node.val <= 5000`
- Follow-up: can you do it both iteratively and recursively?
