---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/binary-tree-postorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-postorder-traversal
---
# Binary Tree Postorder Traversal - Solution

## Intuition

Postorder is left, right, node. If we instead produce node, right, left (a mirrored preorder) and reverse the result, we get left, right, node. Mirrored preorder is easy to do iteratively with a single stack.

## Approach

1. If the tree is empty, return an empty list.
2. Push `root` onto a stack.
3. While the stack is not empty, pop a node and append its value to the result.
4. Push the node's left child, then its right child (if they exist), so the right child is popped first.
5. Reverse the result and return it.

## Code

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = [root]
        visit = [False]
        res = []

        while stack:
            cur, v = stack.pop(), visit.pop()
            if cur:
                if v:
                    res.append(cur.val)
                else:
                    stack.append(cur)
                    visit.append(True)
                    stack.append(cur.right)
                    visit.append(False)
                    stack.append(cur.left)
                    visit.append(False)
        return res
```

## Complexity

- **Time:** `O(n)` — each node is pushed and popped once, and the reversal is linear.
- **Space:** `O(n)` — the stack and result can hold up to `n` values (the stack is `O(h)` in a balanced tree, but the result is always `n`).

## Other Approaches

- **Recursive DFS:** visit left, right, then append the node's value — Time `O(n)` / Space `O(h)` call stack
- **Iterative with last-visited pointer:** walk down the left spine and only visit a node once its right child has been handled — Time `O(n)` / Space `O(h)`
- **Morris traversal:** use temporary threading on a dummy root to avoid the stack — Time `O(n)` / Space `O(1)` extra

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
class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        if(!root) return {}; 

        postorderTraversal(root->left);
        postorderTraversal(root->right);
        result.push_back(root->val);
        
        return result;
    }
private:
    vector<int> result;
};
```
