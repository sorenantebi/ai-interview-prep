---
topic: "Linked List"
difficulty: Easy
leetcode: https://leetcode.com/problems/linked-list-cycle/
neetcode: https://neetcode.io/problems/linked-list-cycle-detection
---
# Linked List Cycle

**Topic:** Linked List · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/linked-list-cycle/) · [NeetCode](https://neetcode.io/problems/linked-list-cycle-detection)

## Problem

Given the `head` of a singly linked list, decide whether the list contains a cycle — i.e. whether following `next` pointers from some node eventually leads back to that same node. Return `true` if a cycle exists, otherwise `false`. (Internally, LeetCode builds the cycle with an index `pos` that the tail connects to; `pos = -1` means no cycle. `pos` is not passed to your function.)

## Examples

**Example 1**
```text
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: the tail links back to the node at index 1.
```

**Example 2**
```text
Input: head = [1,2], pos = 0
Output: true
```

**Example 3**
```text
Input: head = [1], pos = -1
Output: false
```

## Constraints

- The number of nodes is in the range `[0, 10^4]`
- `-10^5 <= Node.val <= 10^5`
- `pos` is `-1` or a valid index in the list
- Follow-up: solve it with `O(1)` extra memory
