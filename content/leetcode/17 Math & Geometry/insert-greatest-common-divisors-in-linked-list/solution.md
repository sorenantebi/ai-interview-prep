---
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/
neetcode: https://neetcode.io/problems/insert-greatest-common-divisors-in-linked-list
---
# Insert Greatest Common Divisors in Linked List - Solution

## Intuition

Each insertion depends only on a node and its original successor, so a single pass is enough. Splice the new node in right after the current one, then jump past it to the original next node so the inserted nodes are never treated as inputs.

## Approach

1. Start with `cur = head`.
2. While `cur.next` exists, compute `g = gcd(cur.val, cur.next.val)`.
3. Create `ListNode(g, cur.next)` and set it as `cur.next`.
4. Advance `cur` by two steps (past the inserted node) to the original next node.
5. Return `head`.

## Code

```python
from typing import List, Optional
from math import gcd

class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        while cur and cur.next:
            cur.next = ListNode(gcd(cur.val, cur.next.val), cur.next)
            # skip the inserted node
            cur = cur.next.next
        return head
```

## Complexity

- **Time:** `O(n log m)` — one pass over `n` nodes, each GCD costs `O(log m)` where `m` is the maximum value (at most 1000).
- **Space:** `O(1)` extra — only pointers are used, apart from the `n - 1` required new nodes in the output.

## Other Approaches

- **Hand-written Euclidean GCD:** replace `math.gcd` with a `while b: a, b = b, a % b` loop — Time `O(n log m)` / Space `O(1)`
- **Recursion:** recurse on `head.next`, inserting the GCD node on the way back — Time `O(n log m)` / Space `O(n)` for the call stack
