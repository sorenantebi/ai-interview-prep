---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/diameter-of-binary-tree/
neetcode: https://neetcode.io/problems/binary-tree-diameter
---
# Diameter of Binary Tree - Solution

**Question:** Diameter of Binary Tree - Question · **Difficulty:** Easy

## Intuition

Any path has a single "highest" node where it turns; its length there is `height(left) + height(right)`. So compute heights bottom-up with a DFS and, at every node, update a global best with the sum of its two child heights.

## Approach

1. Define `dfs(node)` returning the height of `node` in nodes (`0` for null).
2. At each node, get `l = dfs(left)`, `r = dfs(right)`.
3. Update `best = max(best, l + r)` — the longest path bending at this node, in edges.
4. Return `1 + max(l, r)` as this node's height.
5. Call `dfs(root)` and return `best`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        res = 0

        def dfs(root):
            nonlocal res

            if not root:
                return 0
            left = dfs(root.left)
            right = dfs(root.right)
            res = max(res, left + right)

            return 1 + max(left, right)

        dfs(root)
        return res
```

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(h)` — recursion stack (`O(n)` for a skewed tree).

## Other Approaches

- **Height per node (naive):** for every node compute `height(left) + height(right)` with a separate height call — Time `O(n^2)`, Space `O(h)`.

## Key Takeaway

"Return one thing to the parent, update a global answer with another" — the DFS returns a single-branch value (height) while the answer combines both branches. The same pattern solves Binary Tree Maximum Path Sum.

## C++

```cpp
/*
    Given root of binary tree, return length of diameter of tree (longest path b/w any 2 nodes)

    Max path b/w 2 leaf nodes, "1 +" to add path

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
    int diameterOfBinaryTree(TreeNode* root) {
        int result = 0;
        dfs(root, result);
        return result;
    }
private:
    int dfs(TreeNode* root, int& result) {
        if (root == NULL) {
            return 0;
        }
        
        int left = dfs(root->left, result);
        int right = dfs(root->right, result);
        
        result = max(result, left + right);
        return 1 + max(left, right);
    }
};
```
