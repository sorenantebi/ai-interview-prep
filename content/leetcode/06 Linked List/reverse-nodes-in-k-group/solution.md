---
topic: "Linked List"
difficulty: Hard
leetcode: https://leetcode.com/problems/reverse-nodes-in-k-group/
neetcode: https://neetcode.io/problems/reverse-nodes-in-k-group
---
# Reverse Nodes In K Group - Solution

**Question:** Reverse Nodes In K Group - Question · **Difficulty:** Hard

## Intuition

Process the list group by group. Before reversing, check that `k` nodes actually remain (find the `k`-th node from the current group's predecessor); if not, stop. Reverse the group in place and reconnect it between the previous group's tail and the next group's head. A dummy node gives the first group a predecessor.

## Approach

1. `dummy -> head`; `group_prev = dummy`.
2. Find `kth`, the node `k` steps after `group_prev`. If it doesn't exist, break.
3. Let `group_next = kth.next`. Reverse the nodes from `group_prev.next` up to `kth`, initializing `prev = group_next` so the reversed group's tail automatically links to the next group.
4. Reconnect: the old group head (`group_prev.next`) is the new tail; set `group_prev.next = kth` and move `group_prev` to the old head.
5. Return `dummy.next`.

## Code

```python
class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        dummy = ListNode(0, head)
        groupPrev = dummy

        while True:
            kth = self.getKth(groupPrev, k)
            if not kth:
                break
            groupNext = kth.next

            # reverse group
            prev, curr = kth.next, groupPrev.next
            while curr != groupNext:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp

            tmp = groupPrev.next
            groupPrev.next = kth
            groupPrev = tmp
        return dummy.next

    def getKth(self, curr, k):
        while curr and k > 0:
            curr = curr.next
            k -= 1
        return curr
```

## Complexity

- **Time:** `O(n)` — each node is visited a constant number of times (once to count, once to reverse).
- **Space:** `O(1)` — in-place pointer manipulation.

## Other Approaches

- **Recursive:** reverse the first `k` nodes and set the original head's `next` to the recursive result on the rest — Time `O(n)`, Space `O(n/k)` recursion stack.
- **Array of nodes / values:** reverse chunks in an array and rebuild — Time `O(n)`, Space `O(n)`.

## Key Takeaway

For segment reversals, track `group_prev` and `group_next`; initializing `prev = group_next` before reversing stitches the segment's tail for free.
