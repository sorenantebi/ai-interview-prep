---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/delete-node-in-a-bst/
neetcode: https://neetcode.io/problems/delete-node-in-a-bst
---
# Delete Node in a BST - Solution

## Intuition

The BST ordering tells us where to look: go left if `key` is smaller than the current value, right if larger. Once the node is found, there are three cases: no child, one child, or two children. With zero or one child, we simply replace the node by its child (or `None`). With two children, we replace the node's value with its in-order successor (the smallest value in the right subtree) and then delete that successor from the right subtree, which keeps the BST property.

## Approach

1. If the current node is `None`, return `None` (key not found).
2. If `key < root.val`, recurse into the left subtree and reattach the result as `root.left`.
3. If `key > root.val`, recurse into the right subtree and reattach the result as `root.right`.
4. Otherwise this is the node to delete:
   - If it has no left child, return its right child.
   - If it has no right child, return its left child.
   - Otherwise find the minimum node in the right subtree, copy its value into the current node, and delete that value from the right subtree.
5. Return `root`.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return root
        
        if key > root.val:
            root.right = self.deleteNode(root.right, key)
        elif key < root.val:
            root.left = self.deleteNode(root.left, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            # Find the min from right subtree
            cur = root.right
            while cur.left:
                cur = cur.left 
            root.val = cur.val
            root.right = self.deleteNode(root.right, root.val)
        return root
```

## Complexity

- **Time:** `O(h)` — one root-to-node search, plus one walk down to the successor and one deletion of it, each bounded by the tree height `h`.
- **Space:** `O(h)` — recursion stack depth; `O(1)` extra if done iteratively.

## Other Approaches

- **Iterative with parent pointer:** find the node and its parent, splice in the child or successor without recursion — Time `O(h)` / Space `O(1)`
- **Predecessor replacement:** use the maximum of the left subtree instead of the successor; symmetric to the above — Time `O(h)` / Space `O(h)`
- **Rebuild from in-order traversal:** collect all values except `key`, then build a balanced BST — Time `O(n)` / Space `O(n)`

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

// Time: O(h)
// Space: O(1)
class Solution {
public:
    TreeNode* deleteNode(TreeNode* root, int key) {
        if(root == nullptr) return root;

        if(root->val > key) {
            root->left = deleteNode(root->left, key);
        }
        else if(root->val < key) {
            root->right = deleteNode(root->right, key);
        }

        // perform deletion if root->val == key
        else {
            if(!root->left) return root->right;
            if(!root->right) return root->left;

            // both left and right subtrees are not null
            // traverse the right subtree to find the minimum/leftmost value
            // (or) travel the left subtree to find the maximum/rightmost value
            TreeNode* temp = root->right;
            while(temp->left) {
                temp = temp->left;
            }
            root->val = temp->val;

            root->right = deleteNode(root->right, temp->val);
        }

        return root;
    }
};
```
