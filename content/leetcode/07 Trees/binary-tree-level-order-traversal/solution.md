---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/binary-tree-level-order-traversal/
neetcode: https://neetcode.io/problems/level-order-traversal-of-binary-tree
---
# Binary Tree Level Order Traversal - Solution

**Question:** Binary Tree Level Order Traversal - Question · **Difficulty:** Medium

## Intuition

Breadth-first search naturally visits nodes level by level. If, at the start of each round, we record the queue's current length, exactly that many pops belong to the current level — the children they enqueue form the next level.

## Approach

1. If `root` is null, return `[]`; otherwise start a queue with `root`.
2. While the queue is non-empty, let `size = len(queue)`.
3. Pop `size` nodes, collecting their values into `level` and enqueueing their non-null children.
4. Append `level` to the result.
5. Return the result.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        res = []
        q = collections.deque()
        if root:
            q.append(root)

        while q:
            val = []

            for i in range(len(q)):
                node = q.popleft()
                val.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(val)
        return res
```

## Complexity

- **Time:** `O(n)` — each node is enqueued and dequeued once.
- **Space:** `O(w)` — the queue holds at most one level (up to `n/2` nodes); output not counted.

## Other Approaches

- **DFS with depth index:** preorder DFS passing `depth`; append `node.val` to `res[depth]` (creating it when `depth == len(res)`) — Time `O(n)`, Space `O(h)`.

## Key Takeaway

The "`for _ in range(len(q))`" BFS loop is the standard way to process a tree (or grid/graph) one level at a time — reused in right side view, zigzag order, minimum depth, and shortest-path problems.
