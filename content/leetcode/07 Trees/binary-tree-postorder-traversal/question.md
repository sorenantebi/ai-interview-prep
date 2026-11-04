---
video: https://www.youtube.com/watch?v=QhszUQhGGlA
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/binary-tree-postorder-traversal/
neetcode: https://neetcode.io/problems/binary-tree-postorder-traversal
---
# Binary Tree Postorder Traversal

**Topic:** Trees · **Difficulty:** Easy

## Problem

Given the `root` of a binary tree, return the postorder traversal of its nodes' values. In postorder, every node is visited after both of its subtrees: first the left subtree, then the right subtree, then the node itself.

Follow-up: the recursive solution is trivial. Can you do it iteratively?

## Examples

**Example 1**
```text
Input: root = [1,null,2,3]
Output: [3,2,1]
```

**Example 2**
```text
Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
Output: [4,6,7,5,2,9,8,3,1]
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
