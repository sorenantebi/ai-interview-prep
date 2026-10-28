---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/add-two-numbers/
neetcode: https://neetcode.io/problems/add-two-numbers
---
# Add Two Numbers - Solution

**Question:** Add Two Numbers - Question · **Difficulty:** Medium

## Intuition

Since the digits are stored least-significant first, we can simulate grade-school addition directly while walking both lists: add the two digits plus the carry, emit `sum % 10`, carry `sum // 10`. Continue while either list has nodes or a carry remains.

## Approach

1. Create a `dummy` head and `tail`; set `carry = 0`.
2. While `l1`, `l2`, or `carry` is non-zero: take each digit (0 if that list is exhausted), compute `total = d1 + d2 + carry`.
3. Append `ListNode(total % 10)`, set `carry = total // 10`, advance the pointers.
4. Return `dummy.next`.

## Code

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()
        cur = dummy

        carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            # new digit
            val = v1 + v2 + carry
            carry = val // 10
            val = val % 10
            cur.next = ListNode(val)

            # update ptrs
            cur = cur.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next
```

## Complexity

- **Time:** `O(max(m, n))` — one pass over the longer list.
- **Space:** `O(1)` extra — the output list of length `max(m, n) + 1` is not counted.

## Other Approaches

- **Convert to integers:** read both numbers into Python ints, add, then rebuild the list — Time `O(m + n)`, Space `O(m + n)`; works in Python thanks to big ints but defeats the purpose (overflows in fixed-width languages).

## Key Takeaway

Simulate digit-by-digit arithmetic with a carry and loop condition `while l1 or l2 or carry` — it handles unequal lengths and the trailing carry uniformly.

## C++

```cpp
/*
    Given 2 linked lists, digits stored in reverse order, add them
    Ex. l1 = [2,4,3] l2 = [5,6,4] -> [7,0,8] (342 + 465 = 807)

    Sum digit-by-digit + carry, handle if one list becomes null

    Time: O(max(m, n))
    Space: O(max(m, n))
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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* dummy = new ListNode();
        
        ListNode* curr = dummy;
        int carry = 0;
        
        while (l1 != NULL || l2 != NULL) {
            int val1 = (l1 != NULL) ? l1->val : 0;
            int val2 = (l2 != NULL) ? l2->val : 0;
            
            int sum = val1 + val2 + carry;
            carry = sum / 10;
            
            curr->next = new ListNode(sum % 10);
            curr = curr->next;
            
            if (l1 != NULL) {
                l1 = l1->next;
            }
            if (l2 != NULL) {
                l2 = l2->next;
            }
        }
        
        if (carry == 1) {
            curr->next = new ListNode(1);
        }
        
        return dummy->next;
    }
};
```
