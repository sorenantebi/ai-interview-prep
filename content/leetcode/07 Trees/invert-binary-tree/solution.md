---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/invert-binary-tree/
neetcode: https://neetcode.io/problems/invert-a-binary-tree
---
# Invert Binary Tree - Solution

**Question:** Invert Binary Tree - Question · **Difficulty:** Easy

## Intuition

The mirror of a tree is the root with its two subtrees swapped, where each subtree is itself mirrored. That recursive definition maps directly onto a DFS: invert both children, then swap them.

## Approach

1. If `root` is null, return null.
2. Recursively invert `root.left` and `root.right`.
3. Assign the inverted right subtree to `root.left` and the inverted left subtree to `root.right`.
4. Return `root`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        # swap the children
        root.left, root.right = root.right, root.left
        
        # make 2 recursive calls
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(h)` — recursion stack depth equals tree height (`O(n)` worst case for a skewed tree).

## Other Approaches

- **Iterative BFS/DFS:** use a queue or stack; for each popped node swap its children and enqueue them — Time `O(n)`, Space `O(n)` (widest level).

## Key Takeaway

Many tree problems reduce to "do something to the node, recurse on children" — trust the recursive definition and handle the null base case.

## C++

```cpp
/*
    Given the root of a binary tree, invert the tree, and return its root
    Ex. root = [4,2,7,1,3,6,9] -> [4,7,2,9,6,3,1], [2,1,3] -> [2,3,1]

    Preorder traversal, at each node, swap it's left and right children

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
    TreeNode* invertTree(TreeNode* root) {
        if (root == NULL) {
            return NULL;
        }
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};
```
