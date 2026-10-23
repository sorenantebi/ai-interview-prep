---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/copy-list-with-random-pointer/
neetcode: https://neetcode.io/problems/copy-linked-list-with-random-pointer
---
# Copy List With Random Pointer - Solution

**Question:** Copy List With Random Pointer - Question · **Difficulty:** Medium

## Intuition

The difficulty is that a `random` pointer may point to a node whose copy has not been created yet. Splitting the work into two passes solves it: first create a copy of every node and record `original → copy` in a hash map, then wire up `next` and `random` by looking the targets up in the map.

## Approach

1. Initialize `old_to_new = {None: None}` so `null` pointers map to `None` without special cases.
2. Pass 1: for every original node, create `Node(cur.val)` and store it in the map.
3. Pass 2: for every original node, set `copy.next = old_to_new[cur.next]` and `copy.random = old_to_new[cur.random]`.
4. Return `old_to_new[head]`.

## Code

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""


class Solution:
    def copyRandomList(self, head: "Node") -> "Node":
        oldToCopy = {None: None}

        cur = head
        while cur:
            copy = Node(cur.val)
            oldToCopy[cur] = copy
            cur = cur.next
        cur = head
        while cur:
            copy = oldToCopy[cur]
            copy.next = oldToCopy[cur.next]
            copy.random = oldToCopy[cur.random]
            cur = cur.next
        return oldToCopy[head]
```

## Complexity

- **Time:** `O(n)` — two linear passes with `O(1)` dict operations.
- **Space:** `O(n)` — the hash map (excluding the `n` output nodes themselves).

## Other Approaches

- **Interleaving (O(1) extra space):** insert each copy right after its original (`A → A' → B → B'`), set `A'.random = A.random.next`, then unweave the two lists — Time `O(n)`, Space `O(1)` extra.
- **Recursive DFS with memo:** `clone(node)` creates the copy, memoizes it, then recursively clones `next` and `random` — Time `O(n)`, Space `O(n)` (recursion stack can be deep).

## Key Takeaway

For cloning any pointer-based structure (lists with random pointers, graphs), map original nodes to copies first, then connect edges via the map.
