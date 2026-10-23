---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/binary-tree-right-side-view/
neetcode: https://neetcode.io/problems/binary-tree-right-side-view
---
# Binary Tree Right Side View - Solution

**Question:** Binary Tree Right Side View - Question · **Difficulty:** Medium

## Intuition

The visible node on each level is simply the last node of that level in left-to-right order. A level-order BFS gives us each level explicitly, so record the value of the final node popped per level.

## Approach

1. If `root` is null, return `[]`; start a queue with `root`.
2. For each level, pop exactly `len(queue)` nodes, enqueueing left then right children.
3. The last node popped in that level is the rightmost — append its value.
4. Return the collected values.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: TreeNode) -> List[int]:
        res = []
        q = collections.deque([root])

        while q:
            rightSide = None
            qLen = len(q)

            for i in range(qLen):
                node = q.popleft()
                if node:
                    rightSide = node
                    q.append(node.left)
                    q.append(node.right)
            if rightSide:
                res.append(rightSide.val)
        return res
```

## Complexity

- **Time:** `O(n)` — every node is processed once.
- **Space:** `O(w)` — queue holds at most one level; output not counted.

## Other Approaches

- **DFS right-first:** preorder visiting right child before left, appending `node.val` the first time a new depth is reached (`depth == len(res)`) — Time `O(n)`, Space `O(h)`.

## Key Takeaway

"View from a side" problems are level-order problems: take the first (left view) or last (right view) node of each BFS level, or do a DFS that records the first node seen at each depth.
