---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
neetcode: https://neetcode.io/problems/lowest-common-ancestor-in-binary-search-tree
---
# Lowest Common Ancestor of a Binary Search Tree - Solution

**Question:** Lowest Common Ancestor of a Binary Search Tree - Question · **Difficulty:** Medium

## Intuition

The BST ordering tells us where `p` and `q` live relative to any node. If both are smaller than the current node, the LCA is in the left subtree; if both are larger, it is in the right subtree. The first node where they split (or one of them equals the node) is the LCA.

## Approach

1. Start at `cur = root`.
2. If `p.val` and `q.val` are both less than `cur.val`, move to `cur.left`.
3. Else if both are greater than `cur.val`, move to `cur.right`.
4. Otherwise the values diverge here (or one equals `cur`) — return `cur`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    def lowestCommonAncestor(
        self, root: "TreeNode", p: "TreeNode", q: "TreeNode"
    ) -> "TreeNode":
        while True:
            if root.val < p.val and root.val < q.val:
                root = root.right
            elif root.val > p.val and root.val > q.val:
                root = root.left
            else:
                return root
```

## Complexity

- **Time:** `O(h)` — one step down per level (`O(log n)` balanced, `O(n)` skewed).
- **Space:** `O(1)` — iterative, no recursion.

## Other Approaches

- **Generic binary-tree LCA:** post-order DFS returning whichever of `p`/`q` was found in each subtree, ignoring BST order — Time `O(n)`, Space `O(h)`.
- **Recursive BST version:** same decisions as above but recursing — Time `O(h)`, Space `O(h)`.

## Key Takeaway

In a BST, use the ordering to discard half the tree at each step; the LCA is the first node whose value lies between `p` and `q` (inclusive).
