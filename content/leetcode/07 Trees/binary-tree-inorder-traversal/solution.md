---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/binary-tree-inorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-inorder-traversal
---
# Binary Tree Inorder Traversal - Solution

## Intuition

Inorder means left, node, right. To do this without recursion, we simulate the call stack ourselves: keep walking left while pushing nodes onto a stack, and when we can't go further left, pop a node, record it, and move to its right child.

## Approach

1. Initialize an empty result list, an empty stack, and a pointer `curr` set to `root`.
2. While `curr` is not `None` or the stack is non-empty:
   1. Push `curr` onto the stack and move to `curr.left` until `curr` is `None`.
   2. Pop the top node from the stack and append its value to the result.
   3. Set `curr` to the popped node's right child.
3. Return the result.

## Code

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # Iterative
        res, stack = [], []
        cur = root

        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right
        return res

        # Recursive
        res = []

        def helper(root):
            if not root:
                return
            helper(root.left)
            res.append(root.val)
            helper(root.right)

        helper(root)
        return res
```

## Complexity

- **Time:** `O(n)` — each node is pushed and popped exactly once.
- **Space:** `O(h)` — the stack holds at most one root-to-node path, where `h` is the tree height (`O(n)` in the worst case, excluding the output list).

## Other Approaches

- **Recursion:** visit left, append the node, visit right — Time `O(n)` / Space `O(h)` for the call stack
- **Morris Traversal:** temporarily thread each node's inorder predecessor to the node to avoid a stack — Time `O(n)` / Space `O(1)`

## C++

```cpp
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
#include <stack>

class Solution {
public:
    /* Recursive
    vector<int> helper(TreeNode* node, vector<int>& path) {
        if (node == NULL)
            return path;

        path = helper(node->left, path);
        path.push_back(node->val);
        path = helper(node->right, path);
        return path;
    }
    */

    // Iterative
    vector<int> inorderTraversal(TreeNode* root) {
        stack<TreeNode*> stk;
        vector<int> path;
        TreeNode* current = root;

        while (!stk.empty() || current != NULL) {
            while (current != NULL) {
                stk.push(current);
                current = current->left;
            }
            TreeNode* node = stk.top();
            path.push_back(node->val);
            stk.pop();
            current = node->right;
        }
        return path;
    }
};
```
