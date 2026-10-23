---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
neetcode: https://neetcode.io/problems/remove-node-from-end-of-linked-list
---
# Remove Nth Node From End of List

**Topic:** Linked List · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) · [NeetCode](https://neetcode.io/problems/remove-node-from-end-of-linked-list)

## Problem

Given the `head` of a singly linked list and an integer `n`, delete the `n`-th node counting from the end of the list (`n = 1` is the last node) and return the head of the resulting list. `n` is always valid. If the list had a single node, the result is empty.

## Examples

**Example 1**
```text
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
```

**Example 2**
```text
Input: head = [1], n = 1
Output: []
```

**Example 3**
```text
Input: head = [1,2], n = 1
Output: [1]
```

## Constraints

- The number of nodes `sz` is in the range `[1, 30]`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`
- Follow-up: do it in a single pass
