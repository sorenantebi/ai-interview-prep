---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/subtree-of-another-tree/
neetcode: https://neetcode.io/problems/subtree-of-a-binary-tree
---
# Subtree of Another Tree - Solution

**Question:** Subtree of Another Tree - Question · **Difficulty:** Easy

## Intuition

`subRoot` is a subtree of `root` iff it is identical to the tree rooted at some node of `root`. So traverse every node of `root` and run a "same tree" check there; return as soon as one matches.

## Approach

1. Write `same(a, b)`: both null -> true; one null or values differ -> false; else recurse on both children pairs.
2. In `isSubtree(root, subRoot)`: if `root` is null, return false (subRoot is non-empty).
3. If `same(root, subRoot)`, return true.
4. Otherwise return `isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if not subRoot:
            return True
        if not root:
            return False

        if self.isSameTree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if p and q and p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        else:
            return False
```

## Complexity

- **Time:** `O(m * n)` — a same-tree check (up to `n` = size of `subRoot`) may run at each of the `m` nodes of `root`.
- **Space:** `O(h_root + h_sub)` — recursion stacks of both functions.

## Other Approaches

- **Serialize + substring search (KMP / Z-function):** serialize both trees in preorder with null markers and a delimiter before every value (e.g. `,12,N,N`) so `2` cannot match inside `12`, then substring-search — Time `O(m + n)`, Space `O(m + n)`.
- **Merkle hashing:** hash every subtree bottom-up and check whether `subRoot`'s hash appears — Time `O(m + n)` expected, Space `O(m)`.

## Key Takeaway

"Is X somewhere inside Y" on trees = traverse Y and call an equality helper at each node; for linear time, convert trees to strings with unambiguous delimiters and use string matching.
