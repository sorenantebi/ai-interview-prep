---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal
---
# Construct Binary Tree From Preorder And Inorder Traversal

**Topic:** Trees · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) · [NeetCode](https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal)

## Problem

You are given two integer arrays, `preorder` and `inorder`, which are the preorder and inorder traversals of the same binary tree. All values are **unique**. Reconstruct the tree and return its root.

## Examples

**Example 1**
```text
Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
```

**Example 2**
```text
Input: preorder = [-1], inorder = [-1]
Output: [-1]
```

## Constraints

- `1 <= preorder.length <= 3000`
- `inorder.length == preorder.length`
- `-3000 <= preorder[i], inorder[i] <= 3000`
- All values are unique, and both arrays describe the same tree
