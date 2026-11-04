---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/house-robber-iii/
neetcode: https://neetcode.io/problems/house-robber-iii
---
# House Robber III - Solution

## Intuition

For each house there are only two choices: rob it or skip it. If it is robbed, its children must be skipped. If it is skipped, each child is free to be robbed or not, independently. So each subtree only needs to report two numbers: the best total with its root robbed and the best total with its root skipped. Combining these bottom-up solves the problem in one pass.

## Approach

1. Define a post-order helper `dfs(node)` that returns a pair `(rob, skip)`.
2. For a missing node, return `(0, 0)`.
3. Compute the pairs for the left and right children.
4. If the current node is robbed, the children must be skipped: `rob = node.val + left_skip + right_skip`.
5. If the current node is skipped, each child contributes its better option: `skip = max(left_rob, left_skip) + max(right_rob, right_skip)`.
6. The answer is `max(rob, skip)` at the root.

## Code

```python
from typing import List, Optional

class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0, 0
            left_rob, left_skip = dfs(node.left)
            right_rob, right_skip = dfs(node.right)
            rob = node.val + left_skip + right_skip
            skip = max(left_rob, left_skip) + max(right_rob, right_skip)
            return rob, skip

        return max(dfs(root))
```

## Complexity

- **Time:** `O(n)` — each node is visited exactly once and does constant work.
- **Space:** `O(h)` — the recursion stack depth equals the tree height `h`, which is up to `O(n)` for a skewed tree.

## Other Approaches

- **Recursion with memoization:** at each node, take the max of robbing it (plus grandchildren) or skipping it (sum of children), caching results in a hash map — Time `O(n)` / Space `O(n)`
- **Naive recursion:** same choice as above without caching, so subtrees are recomputed — Time `O(2^n)` worst case / Space `O(h)`
