---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/binary-tree-preorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-preorder-traversal
---
# Binary Tree Preorder Traversal - Solution

## Intuition

Preorder means "node, left, right". Using an explicit stack, we can mimic the recursion: pop a node, record it, then push its children so that the left child is processed first. Since a stack is last-in-first-out, the right child must be pushed before the left child.

## Approach

1. If the tree is empty, return an empty list.
2. Initialize a stack with the root and an empty result list.
3. While the stack is not empty, pop a node and append its value to the result.
4. Push the right child (if any), then the left child (if any).
5. Return the result once the stack is empty.

## Code

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        cur, stack = root, []
        res = []
        while cur or stack:
            if cur:
                res.append(cur.val)
                stack.append(cur.right)
                cur = cur.left
            else:
                cur = stack.pop()
        return res
```

## Complexity

- **Time:** `O(n)` — each node is pushed and popped exactly once.
- **Space:** `O(h)` — the stack holds at most the nodes along a path plus pending right siblings, which is `O(n)` in the worst case for a skewed tree (excluding the output list).

## Other Approaches

- **Recursive DFS:** visit the node, then recurse on left and right — Time `O(n)` / Space `O(h)` call stack
- **Morris Traversal:** temporarily thread the tree through predecessor right pointers to avoid a stack — Time `O(n)` / Space `O(1)`

## C++

```cpp
/*
  Given the root of a binary tree, return the preorder traversal of its nodes' values.

  Ex. Input: root = [1,null,2,3]
      Output: [1,2,3]

  Time  : O(N)
  Space : O(H) -> H = Height of the binary tree
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
    vector <int> res;

    vector<int> preorderTraversal(TreeNode* root) {
        if(root != NULL) {
            res.push_back(root -> val);
            preorderTraversal(root -> left);
            preorderTraversal(root -> right);
        }
        return res;
    }
};
```
