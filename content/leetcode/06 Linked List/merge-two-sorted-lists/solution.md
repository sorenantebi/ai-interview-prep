---
topic: "Linked List"
difficulty: Easy
leetcode: https://leetcode.com/problems/merge-two-sorted-lists/
neetcode: https://neetcode.io/problems/merge-two-sorted-linked-lists
---
# Merge Two Sorted Lists - Solution

**Question:** Merge Two Sorted Lists - Question · **Difficulty:** Easy

## Intuition

Like the merge step of merge sort: at each step the smallest remaining value is at the front of one of the two lists. A dummy head node removes the special case of choosing the first node, and once one list runs out the other can be attached in one step.

## Approach

1. Create a `dummy` node and a `tail` pointer to it.
2. While both lists are non-empty, attach the smaller front node to `tail.next` and advance that list and `tail`.
3. Attach whichever list still has nodes (`list1 or list2`) to `tail.next`.
4. Return `dummy.next`.

## Code

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# Iterative
class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        dummy = node = ListNode()

        while list1 and list2:
            if list1.val < list2.val:
                node.next = list1
                list1 = list1.next
            else:
                node.next = list2
                list2 = list2.next
            node = node.next

        node.next = list1 or list2

        return dummy.next
    
# Recursive
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        lil, big = (list1, list2) if list1.val < list2.val else (list2, list1)
        lil.next = self.mergeTwoLists(lil.next, big)
        return lil
```

## Complexity

- **Time:** `O(n + m)` — each node is visited once.
- **Space:** `O(1)` — nodes are re-linked in place; only the dummy node is allocated.

## Other Approaches

- **Recursive:** return the smaller head with its `next` set to the merge of the remainder — Time `O(n + m)`, Space `O(n + m)` recursion stack.

## Key Takeaway

Use a dummy head whenever you build a new list node-by-node; it removes edge cases for the first node and the empty result.
