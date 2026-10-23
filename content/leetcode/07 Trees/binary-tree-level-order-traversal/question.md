---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/binary-tree-level-order-traversal/
neetcode: https://neetcode.io/problems/level-order-traversal-of-binary-tree
---
# Binary Tree Level Order Traversal

**Topic:** Trees · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/binary-tree-level-order-traversal/) · [NeetCode](https://neetcode.io/problems/level-order-traversal-of-binary-tree)

## Problem

Given the `root` of a binary tree, return its node values grouped **level by level**, from top to bottom, with each level listed from left to right. Return a list of lists (one inner list per level); an empty tree gives `[]`.

## Examples

**Example 1**
```text
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
```

**Example 2**
```text
Input: root = [1]
Output: [[1]]
```

**Example 3**
```text
Input: root = []
Output: []
```

## Constraints

- The number of nodes is in the range `[0, 2000]`
- `-1000 <= Node.val <= 1000`
