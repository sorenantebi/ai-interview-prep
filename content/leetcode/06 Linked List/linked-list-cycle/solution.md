---
topic: "Linked List"
difficulty: Easy
leetcode: https://leetcode.com/problems/linked-list-cycle/
neetcode: https://neetcode.io/problems/linked-list-cycle-detection
---
# Linked List Cycle - Solution

**Question:** Linked List Cycle - Question · **Difficulty:** Easy

## Intuition

Floyd's tortoise and hare: move one pointer one step at a time and another two steps at a time. If there is no cycle, the fast pointer reaches the end. If there is a cycle, both pointers end up inside it and the fast one gains one node per step on the slow one, so they must meet.

## Approach

1. Start `slow` and `fast` at `head`.
2. While `fast` and `fast.next` exist: move `slow` one step and `fast` two steps.
3. If they ever point to the same node, return `True`.
4. If the loop exits (end of list reached), return `False`.

## Code

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow, fast = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
```

## Complexity

- **Time:** `O(n)` — the fast pointer either exits in `n/2` steps or catches the slow one within one lap of the cycle.
- **Space:** `O(1)` — two pointers.

## Other Approaches

- **Hash set of visited nodes:** return `True` when a node is seen twice — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Fast/slow pointers detect cycles in `O(1)` space; the same idea finds the middle of a list and the cycle start (Linked List Cycle II, Find the Duplicate Number).

## C++

```cpp
/*
    Given head of a linked list, determine if it has a cycle in it

    Slow/fast pointers, if they ever intersect then there's a cycle

    Time: O(n)
    Space: O(1)
*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    bool hasCycle(ListNode *head) {
        if (head == NULL) {
            return false;
        }
        
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast->next != NULL && fast->next->next != NULL) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                return true;
            }
        }
        
        return false;
    }
};
```
