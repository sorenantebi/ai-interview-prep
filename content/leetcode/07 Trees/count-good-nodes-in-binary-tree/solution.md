---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/count-good-nodes-in-binary-tree/
neetcode: https://neetcode.io/problems/count-good-nodes-in-binary-tree
---
# Count Good Nodes In Binary Tree - Solution

**Question:** Count Good Nodes In Binary Tree - Question · **Difficulty:** Medium

## Intuition

Whether a node is good depends only on the maximum value seen on the path from the root to it. So carry that running maximum down a DFS: a node is good iff `node.val >= path_max`, and its children inherit `max(path_max, node.val)`.

## Approach

1. Push `(root, root.val)` onto a stack (the root's path max is itself).
2. Pop `(node, mx)`; if `node.val >= mx`, count it.
3. Compute `mx = max(mx, node.val)` and push each non-null child with this new `mx`.
4. Return the count when the stack is empty.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, maxVal):
            if not node:
                return 0

            res = 1 if node.val >= maxVal else 0
            maxVal = max(maxVal, node.val)
            res += dfs(node.left, maxVal)
            res += dfs(node.right, maxVal)
            return res

        return dfs(root, root.val)
```

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(h)` — the explicit stack (`O(n)` worst case); iterative to avoid recursion limits on 10^5-node chains.

## Other Approaches

- **Recursive DFS:** `dfs(node, mx)` returning `(node.val >= mx) + dfs(left, new_mx) + dfs(right, new_mx)` — Time `O(n)`, Space `O(h)` recursion.
- **BFS with `(node, mx)` pairs:** same logic with a queue — Time `O(n)`, Space `O(w)`.

## Key Takeaway

When a node's property depends on its ancestors, pass the needed summary (max, min, sum, bounds) **down** the traversal as a parameter.
