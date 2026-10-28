---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal
---
# Construct Binary Tree From Preorder And Inorder Traversal - Solution

**Question:** Construct Binary Tree From Preorder And Inorder Traversal - Question · **Difficulty:** Medium

## Intuition

The first preorder value is always the root. Its position in `inorder` splits the inorder array into the left subtree (everything before) and right subtree (everything after). Because preorder lists the whole left subtree before the right one, we can consume preorder left to right with a single pointer while recursing on inorder index ranges; a hashmap gives `O(1)` root lookups.

## Approach

1. Build `pos[value] = index in inorder`.
2. Keep a pointer `pre_i` into `preorder` (starts at 0).
3. `build(lo, hi)` constructs the subtree whose inorder range is `[lo, hi]`:
   - if `lo > hi`, return null;
   - root value = `preorder[pre_i]`, advance `pre_i`;
   - `mid = pos[root value]`; build left from `[lo, mid-1]`, then right from `[mid+1, hi]` (left first, matching preorder).
4. Return `build(0, n-1)`.

## Code

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])
        return root
```

## Complexity

- **Time:** `O(n)` — each node is created once with `O(1)` index lookup.
- **Space:** `O(n)` — the hashmap, plus `O(h)` recursion stack.

## Other Approaches

- **Slicing recursion:** `root = preorder[0]`, `mid = inorder.index(root)`, recurse on list slices — Time `O(n^2)`, Space `O(n^2)` from copies; simple but slow.
- **Iterative stack:** push preorder nodes, popping while the stack top matches the current inorder value to know when to attach a right child — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Preorder (or postorder) identifies the root; inorder tells you how many nodes go left vs. right. A value-to-index hashmap plus a moving preorder pointer makes the reconstruction linear.

## C++

```cpp
/*
    Given 2 integer arrays preorder & inorder, construct & return the binary tree
    Ex. preorder = [3,9,20,15,7], inorder = [9,3,15,20,7] -> [3,9,20,null,null,15,7]

    Preorder dictates nodes, inorder dictates subtrees (preorder values, inorder positions)

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
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        int index = 0;
        return build(preorder, inorder, index, 0, inorder.size() - 1);
    }
private:
    TreeNode* build(vector<int>& preorder, vector<int>& inorder, int& index, int i, int j) {
        if (i > j) {
            return NULL;
        }
        
        TreeNode* root = new TreeNode(preorder[index]);
        
        int split = 0;
        for (int i = 0; i < inorder.size(); i++) {
            if (preorder[index] == inorder[i]) {
                split = i;
                break;
            }
        }
        index++;
        
        root->left = build(preorder, inorder, index, i, split - 1);
        root->right = build(preorder, inorder, index, split + 1, j);
        
        return root;
    }
};
```
