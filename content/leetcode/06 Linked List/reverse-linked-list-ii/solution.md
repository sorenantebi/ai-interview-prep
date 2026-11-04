---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/reverse-linked-list-ii/
neetcode: https://neetcode.io/problems/reverse-linked-list-ii
---
# Reverse Linked List II - Solution

## Intuition

Only the sublist between `left` and `right` changes. If we stand on the node just before position `left`, we can repeatedly take the node after the current sublist head and move it to the front of the sublist. After `right - left` such moves, the segment is reversed, all in a single pass and with no extra memory.

A dummy node before `head` handles the case `left == 1` without special code.

## Approach

1. Create a `dummy` node pointing to `head`.
2. Walk `prev` forward `left - 1` steps so it sits just before the segment.
3. Let `cur = prev.next`; this node will end up as the tail of the reversed segment.
4. Repeat `right - left` times: detach `nxt = cur.next` and insert it right after `prev`.
5. Return `dummy.next`.

## Code

```python
class Solution:
    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:
        dummy = ListNode(0, head)

        # 1) reach node at position "left"
        leftPrev, cur = dummy, head
        for i in range(left - 1):
            leftPrev, cur = cur, cur.next

        # Now cur="left", leftPrev="node before left"
        # 2) reverse from left to right
        prev = None
        for i in range(right - left + 1):
            tmpNext = cur.next
            cur.next = prev
            prev, cur = cur, tmpNext

        # 3) Update pointers
        leftPrev.next.next = cur  # cur is node after "right"
        leftPrev.next = prev  # prev is "right"
        return dummy.next
```

## Complexity

- **Time:** `O(n)` — one traversal to reach the segment plus at most `right - left` pointer moves.
- **Space:** `O(1)` — only a constant number of pointers are used.

## Other Approaches

- **Standard reversal with reconnection:** walk to the segment, reverse it like a normal list reversal, then stitch the ends back together — Time `O(n)` / Space `O(1)`
- **Recursive reversal:** recurse to the segment and reverse it on the way back — Time `O(n)` / Space `O(n)` for the call stack
- **Array copy:** store values in an array, reverse the slice, write back — Time `O(n)` / Space `O(n)`

## C++

```cpp
/*
    Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.
    
    Time complexity: O(n)
    Space complexity: O(1)
*/
class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode* dummy = new ListNode();
        dummy->next = head;

        int i=0;
        ListNode* leftConnector = dummy,*temp = head;
        while(i<left-1){
            leftConnector = temp;
            temp = temp->next;
            i++;
        }
        ListNode* prev = NULL;
        i=0;
        while(i<right-left+1){
            ListNode* store = temp->next;
            temp->next = prev;
            prev = temp;
            temp = store;
            i++;
        }
        leftConnector->next->next = temp;
        leftConnector->next = prev;

        return dummy->next;
    }
};
```
