---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/insert-into-a-binary-search-tree/
neetcode: https://neetcode.io/problems/insert-into-a-binary-search-tree
---
# Insert into a Binary Search Tree - Solution

## Intuition

A new value can always be attached as a leaf. Following the BST ordering rule (smaller goes left, larger goes right) from the root leads to exactly one empty slot where the value belongs. Place a new node there.

## Approach

1. If the tree is empty, return a new node holding `val`.
2. Start at the root and walk down: go left if `val < cur.val`, otherwise go right.
3. When the chosen child is `None`, attach the new node there and stop.
4. Return the original root.

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return TreeNode(val)
        if val > root.val:
            root.right = self.insertIntoBST(root.right, val)
        else:
            root.left = self.insertIntoBST(root.left, val)
        return root
```

## Complexity

- **Time:** `O(h)` — one step per level, where `h` is the tree height (`O(log n)` balanced, `O(n)` skewed).
- **Space:** `O(1)` — iterative, no extra memory beyond the new node.

## Other Approaches

- **Recursive:** recurse into the left or right subtree and assign the returned subtree root back to the child pointer — Time `O(h)` / Space `O(h)` for the call stack.
- **Rebuild with rotations (e.g. AVL/Red-Black):** insert and rebalance to keep the tree height logarithmic — Time `O(log n)` / Space `O(1)` iterative or `O(log n)` recursive.

## C++

```cpp
/*
    You are given the root node of a binary search tree (BST) and a value to insert into the tree. 
    Return the root node of the BST after the insertion. It is guaranteed that the new value does not exist in the original BST.

    Notice that there may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. 
    You can return any of them.

    Ex. Input: root = [4,2,7,1,3], val = 5
        Output: [4,2,7,1,3,5]

    Time  : O(N)
    Space : O(N)
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
    TreeNode * create(int val) {
        TreeNode *n = new TreeNode;
        n -> val = val;
        n -> left = n -> right = NULL;
        return n;
    }

    TreeNode* insertIntoBST(TreeNode* root, int val) {
        if(root == NULL) 
		    return create(val);

        else if(val > root -> val)
		    root -> right = insertIntoBST(root -> right, val); 
        else if(val < root -> val)
		    root -> left = insertIntoBST(root -> left, val);
	    return root;
    }
};
```
