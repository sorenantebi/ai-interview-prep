---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/validate-binary-search-tree/
neetcode: https://neetcode.io/problems/valid-binary-search-tree
---
# Validate Binary Search Tree - Solution

**Question:** Validate Binary Search Tree - Question · **Difficulty:** Medium

## Intuition

Comparing a node only with its direct children is not enough — every node must respect **all** its ancestors. Track an open interval `(low, high)` of allowed values: going left tightens the upper bound to the parent's value, going right tightens the lower bound.

## Approach

1. Start with `(root, -inf, +inf)` on a stack.
2. Pop `(node, low, high)`; if `node` is null, continue.
3. If not `low < node.val < high`, return `false`.
4. Push `(node.left, low, node.val)` and `(node.right, node.val, high)`.
5. If the stack empties without a violation, return `true`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def valid(node, left, right):
            if not node:
                return True
            if not (left < node.val < right):
                return False

            return valid(node.left, left, node.val) and valid(
                node.right, node.val, right
            )

        return valid(root, float("-inf"), float("inf"))
```

## Complexity

- **Time:** `O(n)` — each node is checked once.
- **Space:** `O(h)` — the stack holds pending nodes along the current path plus siblings (`O(n)` worst case).

## Other Approaches

- **Inorder traversal:** a BST's inorder sequence is strictly increasing; compare each value with the previous one — Time `O(n)`, Space `O(h)`.
- **Recursive bounds DFS:** `valid(node, low, high)` — same logic, Time `O(n)`, Space `O(h)` recursion.

## Key Takeaway

BST validity is a global constraint — propagate `(min, max)` bounds down the tree (or check that inorder is strictly increasing) instead of only comparing parent and child.

## C++

```cpp
/*
    Given root of binary tree, determine if it's valid (left all < curr, right all > curr)
    
    Inorder traversal & check if prev >= curr, recursive/iterative solutions
    
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
    bool isValidBST(TreeNode* root) {
        return helper(root, LONG_MIN, LONG_MAX);
    }
private:
    bool helper(TreeNode* root, long left, long right){
        if (!root)
            return true;
        if (root->val < right && root->val > left){
            return helper(root->left, left, root->val) && helper(root->right, root->val, right);
        }
        return false;
    }
};
/*
class Solution {
public:
    bool isValidBST(TreeNode* root) {
        TreeNode* prev = NULL;
        return inorder(root, prev);
    }
private:
    bool inorder(TreeNode* root, TreeNode*& prev) {
        if (root == NULL) {
            return true;
        }
        
        if (!inorder(root->left, prev)) {
            return false;
        }
        
        if (prev != NULL && prev->val >= root->val) {
            return false;
        }
        prev = root;
        
        if (!inorder(root->right, prev)) {
            return false;
        }
        
        return true;
    }
};
*/

// class Solution {
// public:
//     bool isValidBST(TreeNode* root) {
//         stack<TreeNode*> stk;
//         TreeNode* prev = NULL;
        
//         while (!stk.empty() || root != NULL) {
//             while (root != NULL) {
//                 stk.push(root);
//                 root = root->left;
//             }
//             root = stk.top();
//             stk.pop();
            
//             if (prev != NULL && prev->val >= root->val) {
//                 return false;
//             }
            
//             prev = root;
//             root = root->right;
//         }
        
//         return true;
//     }
// };
```
