---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/delete-leaves-with-a-given-value/
neetcode: https://neetcode.io/problems/delete-leaves-with-a-given-value
---
# Delete Leaves With a Given Value - Solution

## Intuition

A node can only become a leaf after its children have been processed. So we should handle the children first and decide about the node afterwards, which is exactly a post-order traversal.

## Approach

1. If the node is `None`, return `None`.
2. Recursively process the left and right subtrees and reassign `node.left` and `node.right` to the returned results.
3. After the children are processed, check whether the node is now a leaf (no left and no right child) and its value equals `target`. If so, return `None` to delete it.
4. Otherwise return the node itself.
5. The value returned for the root is the new root of the tree.

## Code

```python
from typing import List, Optional

class Solution:
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        if not root:
            return None

        root.left = self.removeLeafNodes(root.left, target)
        root.right = self.removeLeafNodes(root.right, target)

        # children are already pruned, so this check also catches newly created leaves
        if not root.left and not root.right and root.val == target:
            return None
        return root
```

## Complexity

- **Time:** `O(n)` — each node is visited exactly once.
- **Space:** `O(h)` — recursion stack depth equals the tree height, which is `O(n)` in the worst case (skewed tree) and `O(log n)` for a balanced tree.

## Other Approaches

- **Iterative post-order with a stack:** simulate the post-order traversal with an explicit stack and parent tracking to avoid recursion depth limits — Time `O(n)` / Space `O(h)`
- **Repeated leaf removal passes:** repeatedly scan the tree and delete target leaves until nothing changes — Time `O(n·h)` / Space `O(h)`
