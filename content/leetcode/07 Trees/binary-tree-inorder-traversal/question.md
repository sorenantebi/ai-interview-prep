---
video: https://www.youtube.com/watch?v=g_S5WuasWUE
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/binary-tree-inorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-inorder-traversal
---
# Binary Tree Inorder Traversal

**Topic:** Trees · **Difficulty:** Easy

## Problem

Given the `root` of a binary tree, return the inorder traversal of its nodes' values. In an inorder traversal, you visit the left subtree first, then the node itself, and finally the right subtree.

**Follow up:** The recursive solution is trivial. Can you do it iteratively?

## Examples

**Example 1**
```text
Input: root = [1,null,2,3]
Output: [1,3,2]
```

**Example 2**
```text
Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
Output: [4,2,6,5,7,1,3,9,8]
```

**Example 3**
```text
Input: root = []
Output: []
```

**Example 4**
```text
Input: root = [1]
Output: [1]
```

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`
