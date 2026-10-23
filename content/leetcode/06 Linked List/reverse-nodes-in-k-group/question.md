---
topic: "Linked List"
difficulty: Hard
leetcode: https://leetcode.com/problems/reverse-nodes-in-k-group/
neetcode: https://neetcode.io/problems/reverse-nodes-in-k-group
---
# Reverse Nodes In K Group

**Topic:** Linked List · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/reverse-nodes-in-k-group/) · [NeetCode](https://neetcode.io/problems/reverse-nodes-in-k-group)

## Problem

Given the `head` of a linked list and a positive integer `k`, reverse the nodes of the list in consecutive groups of `k` and return the new head. If the number of remaining nodes at the end is less than `k`, leave that final partial group in its original order. You must relink the nodes, not just change their values.

## Examples

**Example 1**
```text
Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]
```

**Example 2**
```text
Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]
```

## Constraints

- The number of nodes is `n`, with `1 <= k <= n <= 5000`
- `0 <= Node.val <= 1000`
- Follow-up: solve it with `O(1)` extra memory
