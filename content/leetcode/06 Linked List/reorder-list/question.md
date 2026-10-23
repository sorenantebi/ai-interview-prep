---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/reorder-list/
neetcode: https://neetcode.io/problems/reorder-linked-list
---
# Reorder List

**Topic:** Linked List · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/reorder-list/) · [NeetCode](https://neetcode.io/problems/reorder-linked-list)

## Problem

You are given the `head` of a singly linked list whose nodes are, in order, `L0 → L1 → … → Ln-1 → Ln`. Rearrange the nodes in place so the order becomes `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …` (alternately taking from the front and the back). You must re-link the nodes themselves, not just change their values. The function returns nothing.

## Examples

**Example 1**
```text
Input: head = [1,2,3,4]
Output: [1,4,2,3]
```

**Example 2**
```text
Input: head = [1,2,3,4,5]
Output: [1,5,2,4,3]
```

## Constraints

- The number of nodes is in the range `[1, 5 * 10^4]`
- `1 <= Node.val <= 1000`
