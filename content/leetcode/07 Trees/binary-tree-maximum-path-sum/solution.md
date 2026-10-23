---
topic: "Trees"
difficulty: Hard
leetcode: https://leetcode.com/problems/binary-tree-maximum-path-sum/
neetcode: https://neetcode.io/problems/binary-tree-maximum-path-sum
---
# Binary Tree Maximum Path Sum - Solution

**Question:** Binary Tree Maximum Path Sum - Question · **Difficulty:** Hard

## Intuition

Every path has one highest node where it may bend, using a downward branch on each side. A post-order DFS can return, for each node, the best **single downward branch** starting there (`node.val + max(0, left_branch, right_branch)` — negative branches are dropped). At the same node, the best path bending there is `node.val + max(0, left) + max(0, right)`, which updates a global maximum.

## Approach

1. Initialize `best = root.val` (a path must have at least one node).
2. `gain(node)`: return `0` for null.
3. Compute `l = max(gain(left), 0)` and `r = max(gain(right), 0)` — ignore branches that would reduce the sum.
4. Update `best = max(best, node.val + l + r)` (path bending at this node).
5. Return `node.val + max(l, r)` — only one branch can continue upward to the parent.
6. Call `gain(root)` and return `best`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        res = [root.val]

        # return max path sum without split
        def dfs(root):
            if not root:
                return 0

            leftMax = dfs(root.left)
            rightMax = dfs(root.right)
            leftMax = max(leftMax, 0)
            rightMax = max(rightMax, 0)

            # compute max path sum WITH split
            res[0] = max(res[0], root.val + leftMax + rightMax)
            return root.val + max(leftMax, rightMax)

        dfs(root)
        return res[0]
```

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(h)` — recursion stack.

## Other Approaches

- **Brute force over every bend point:** for each node, separately compute the best downward path in each subtree — Time `O(n^2)`, Space `O(h)`.

## Key Takeaway

Same skeleton as Diameter of Binary Tree: the DFS **returns** the best one-sided extension while it **records** the best two-sided combination; clamp negative contributions to zero.
