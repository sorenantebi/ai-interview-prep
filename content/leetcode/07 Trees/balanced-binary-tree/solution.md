---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/balanced-binary-tree/
neetcode: https://neetcode.io/problems/balanced-binary-tree
---
# Balanced Binary Tree - Solution

**Question:** Balanced Binary Tree - Question · **Difficulty:** Easy

## Intuition

Checking balance top-down recomputes heights repeatedly. Instead, compute heights bottom-up and use a sentinel (`-1`) to signal "some subtree below is already unbalanced", so the whole check finishes in one pass.

## Approach

1. Define `height(node)`: return `0` for null.
2. Recursively get the left and right heights; if either is `-1`, propagate `-1`.
3. If `|left - right| > 1`, return `-1`.
4. Otherwise return `1 + max(left, right)`.
5. The tree is balanced iff `height(root) != -1`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def dfs(root):
            if not root:
                return [True, 0]

            left, right = dfs(root.left), dfs(root.right)
            balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1
            return [balanced, 1 + max(left[1], right[1])]

        return dfs(root)[0]
```

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(h)` — recursion stack.

## Other Approaches

- **Top-down:** at each node compare `height(left)` and `height(right)` then recurse into both children — Time `O(n log n)` balanced / `O(n^2)` skewed, Space `O(h)`.

## Key Takeaway

When a check depends on subtree heights, compute them post-order and fold the validity flag into the return value (sentinel or `(ok, height)` tuple) to stay linear.

## C++

```cpp
/*
    Given binary tree, determine if height-balanced (all left & right subtrees height diff <= 1)

    Check if subtrees are balanced, if so, use their heights to determine further balance

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
    bool isBalanced(TreeNode* root) {
        int height = 0;
        return dfs(root, height);
    }
private:
    bool dfs(TreeNode* root, int& height) {
        if (root == NULL) {
            height = -1;
            return true;
        }
        
        int left = 0;
        int right = 0;
        
        if (!dfs(root->left, left) || !dfs(root->right, right)) {
            return false;
        }
        if (abs(left - right) > 1) {
            return false;
        }
        
        height = 1 + max(left, right);
        return true;
    }
};
```
