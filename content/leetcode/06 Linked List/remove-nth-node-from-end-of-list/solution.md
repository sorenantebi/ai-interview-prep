---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
neetcode: https://neetcode.io/problems/remove-node-from-end-of-linked-list
---
# Remove Nth Node From End of List - Solution

**Question:** Remove Nth Node From End of List - Question · **Difficulty:** Medium

## Intuition

To delete a node we need the node *before* it. If a `right` pointer is `n` steps ahead of a `left` pointer, then when `right` reaches the end, `left` is exactly at the node to remove (or just before it). Starting `left` at a dummy node placed before `head` makes it land on the predecessor and also handles removing the head itself.

## Approach

1. Create `dummy` with `dummy.next = head`; set `left = dummy`, `right = head`.
2. Advance `right` by `n` nodes.
3. Move both pointers together until `right` is `None`; now `left.next` is the target.
4. Skip it: `left.next = left.next.next`. Return `dummy.next`.

## Code

```python
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(0, head)
        left = dummy
        right = head

        while n > 0:
            right = right.next
            n -= 1

        while right:
            left = left.next
            right = right.next

        # delete
        left.next = left.next.next
        return dummy.next
```

## Complexity

- **Time:** `O(sz)` — a single pass over the list.
- **Space:** `O(1)` — two pointers and a dummy node.

## Other Approaches

- **Two passes:** count the length `L`, then walk `L - n` steps to the predecessor — Time `O(sz)`, Space `O(1)`.

## Key Takeaway

A fixed-size gap between two pointers converts "k-th from the end" into a one-pass problem; a dummy head removes the "delete the head" edge case.

## C++

```cpp
/*
    Given head of a linked list, remove nth node from end of list
    Ex. head = [1,2,3,4,5], n = 2 -> [1,2,3,5]

    Create 2 pointers "n" apart, iterate until end, will be at nth

    Time: O(n)
    Space: O(1)
*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        if (head->next == NULL) {
            return NULL;
        }
        
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (n > 0) {
            fast = fast->next;
            n--;
        }
        
        if (fast == NULL) {
            return head->next;
        }
        
        while (fast->next != NULL) {
            slow = slow->next;
            fast = fast->next;
        }
        
        slow->next = slow->next->next;
        return head;
    }
};
```
