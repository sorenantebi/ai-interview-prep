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

## C++

```cpp
/*
    Given heads of 2 sorted linked lists, merge into 1 sorted list
    Ex. list1 = [1,2,4], list2 = [1,3,4] -> [1,1,2,3,4,4]

    Create curr pointer, iterate thru, choose next to be lower one

    Time: O(m + n)
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
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (list1 == NULL && list2 == NULL) {
            return NULL;
        }
        if (list1 == NULL) {
            return list2;
        }
        if (list2 == NULL) {
            return list1;
        }
        
        ListNode* dummy = new ListNode();
        ListNode *curr = dummy;
        while (list1 != NULL && list2 != NULL) {
            if (list1->val <= list2->val) {
                curr->next = list1;
                list1 = list1->next;
            } else {
                curr->next = list2;
                list2 = list2->next;
            }
            curr = curr->next;
        }
        
        if (list1 == NULL) {
            curr->next = list2;
        } else {
            curr->next = list1;
        }
        
        return dummy->next;
    }
};
```
