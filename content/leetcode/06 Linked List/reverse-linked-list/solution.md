---
topic: "Linked List"
difficulty: Easy
leetcode: https://leetcode.com/problems/reverse-linked-list/
neetcode: https://neetcode.io/problems/reverse-a-linked-list
---
# Reverse Linked List - Solution

**Question:** Reverse Linked List - Question · **Difficulty:** Easy

## Intuition

Walking the list once, we can flip each node's `next` pointer to point backwards. The only subtlety is that flipping a pointer loses the link to the rest of the list, so we save `next` before overwriting it. Three pointers (`prev`, `cur`, `nxt`) are enough.

## Approach

1. Set `prev = None` and `cur = head`.
2. While `cur` is not `None`: save `nxt = cur.next`, point `cur.next = prev`, then advance `prev = cur`, `cur = nxt`.
3. When `cur` falls off the end, `prev` is the new head; return it.

## Code

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev, curr = None, head

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev
```

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(1)` — only a few pointers; the list is reversed in place.

## Other Approaches

- **Recursive:** reverse the rest of the list, then set `head.next.next = head` and `head.next = None` — Time `O(n)`, Space `O(n)` recursion stack.
- **Stack / array:** push values onto a stack and rebuild — Time `O(n)`, Space `O(n)`.

## Key Takeaway

The `prev / cur / nxt` pointer dance is the building block for many linked-list problems (Reorder List, Reverse Linked List II, K-Group reversal) — memorize it.

## C++

```cpp
/*
    Given the head of a singly linked list, reverse list & return
    Ex. head = [1,2,3,4,5] -> [5,4,3,2,1], head = [1,2] -> [2,1]

    Maintain prev, curr pointers, iterate thru & reverse

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
class Solution
{
public:
    ListNode *reverseList(ListNode *head)
    {
        if (head == NULL || head->next == NULL)
            return head;

        ListNode *prev = NULL;
        ListNode *curr = head;

        while (curr != NULL)
        {
            ListNode *temp = curr->next;
            curr->next = prev;
            prev = curr;
            curr = temp;
        }
        return prev;
    }
};
```
