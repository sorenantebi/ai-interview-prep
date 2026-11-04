---
video: https://www.youtube.com/watch?v=afTpieEZXck
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/binary-tree-preorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-preorder-traversal
---
# Binary Tree Preorder Traversal

**Topic:** Trees · **Difficulty:** Easy

## Problem

Given the `root` of a binary tree, return the preorder traversal of its nodes' values. In a preorder traversal, each node is visited before its left subtree, and the left subtree is visited before the right subtree.

Follow up: a recursive solution is trivial. Can you do it iteratively?

## Examples

**Example 1**
```text
Input: root = [1,null,2,3]
Output: [1,2,3]
```

**Example 2**
```text
Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
Output: [1,2,4,5,6,7,3,8,9]
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
