---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/reorder-list/
neetcode: https://neetcode.io/problems/reorder-linked-list
---
# Reorder List - Solution

**Question:** Reorder List - Question · **Difficulty:** Medium

## Intuition

The target order interleaves the first half with the *reversed* second half. So the problem decomposes into three classic linked-list primitives: find the middle (fast/slow pointers), reverse the second half, and merge two lists alternately.

## Approach

1. Find the middle with `slow`/`fast` pointers (`fast` starts at `head.next` so `slow` ends at the end of the first half).
2. Cut the list after `slow` and reverse the second half.
3. Merge alternately: take one node from the first half, then one from the reversed second half, until the second half is exhausted (the first half is equal or one longer).

## Code

```python
class Solution:
    def reorderList(self, head: ListNode) -> None:
        # find middle
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # reverse second half
        second = slow.next
        prev = slow.next = None
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp

        # merge two halfs
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2
```

## Complexity

- **Time:** `O(n)` — three linear passes (middle, reverse, merge).
- **Space:** `O(1)` — all re-linking is done in place.

## Other Approaches

- **Array of nodes + two pointers:** store nodes in a list, then link `i` and `j` from both ends inward — Time `O(n)`, Space `O(n)`.
- **Stack / deque:** push nodes onto a deque and pop alternately from both ends — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Many "hard-looking" list problems are compositions of three primitives: find middle, reverse, merge. Recognize the decomposition and reuse the standard snippets.

## C++

```cpp
/*
    Given head of linked-list, reorder list alternating outside in
    Ex. head = [1,2,3,4] -> [1,4,2,3], head = [1,2,3,4,5] -> [1,5,2,4,3]

    Find middle node, split in half, reverse 2nd half of list, merge

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
    void reorderList(ListNode* head) {
        if (head->next == NULL) {
            return;
        }
        
        ListNode* prev = NULL;
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast != NULL && fast->next != NULL) {
            prev = slow;
            slow = slow->next;
            fast = fast->next->next;
        }
        
        prev->next = NULL;
        
        ListNode* l1 = head;
        ListNode* l2 = reverse(slow);
        
        merge(l1, l2);
    }
private:
    ListNode* reverse(ListNode* head) {
        ListNode* prev = NULL;
        ListNode* curr = head;
        ListNode* next = curr->next;
        
        while (curr != NULL) {
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        
        return prev;
    }
    void merge(ListNode* l1, ListNode* l2) {
        while (l1 != NULL) {
            ListNode* p1 = l1->next;
            ListNode* p2 = l2->next;
            
            l1->next = l2;
            if (p1 == NULL) {
                break;
            }
            l2->next = p1;
            
            l1 = p1;
            l2 = p2;
        }
    }
};
```
