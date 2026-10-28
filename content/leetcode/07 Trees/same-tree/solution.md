---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/same-tree/
neetcode: https://neetcode.io/problems/same-binary-tree
---
# Same Tree - Solution

**Question:** Same Tree - Question · **Difficulty:** Easy

## Intuition

Two trees are equal iff their roots match and their left subtrees are equal and their right subtrees are equal. A simultaneous DFS over both trees checks that, bailing out at the first mismatch in shape or value.

## Approach

1. If both nodes are null, return `true`.
2. If exactly one is null, or their values differ, return `false`.
3. Return `isSameTree(p.left, q.left) and isSameTree(p.right, q.right)`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if p and q and p.val == q.val:
            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        else:
            return False
```

## Complexity

- **Time:** `O(min(n, m))` — stops at the first mismatch; at most visits every node of the smaller tree.
- **Space:** `O(min(h1, h2))` — recursion stack.

## Other Approaches

- **Iterative BFS on pairs:** push `(p, q)` pairs into a queue and compare each pair — Time `O(n)`, Space `O(w)`.
- **Serialize and compare:** serialize both with explicit null markers and compare strings — Time `O(n + m)`, Space `O(n + m)`.

## Key Takeaway

The "walk two trees in lockstep" recursion is a building block for Subtree of Another Tree, Symmetric Tree, and Merge Two Binary Trees.

## C++

```cpp
/*
    Given roots of 2 binary trees, check if they're the same or not (same structure & values)
    Ex. p = [1,2,3] q = [1,2,3] -> true, p = [1,2] q = [1,null,2] -> false

    Check: (1) matching nulls, (2) non-matching nulls, (3) non-matching values

    Time: O(n)
    Space: O(n)
*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (p == NULL && q == NULL) {
            return true;
        }
        if (p == NULL || q == NULL) {
            return false;
        }
        if (p->val != q->val) {
            return false;
        }
        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};
```
