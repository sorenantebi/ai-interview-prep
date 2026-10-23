---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/balanced-binary-tree/
neetcode: https://neetcode.io/problems/balanced-binary-tree
---
# Balanced Binary Tree

**Topic:** Trees · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/balanced-binary-tree/) · [NeetCode](https://neetcode.io/problems/balanced-binary-tree)

## Problem

Given a binary tree, decide whether it is **height-balanced**: for **every** node, the heights of its left and right subtrees differ by at most `1`. Return `true` if so, otherwise `false`. An empty tree is balanced.

## Examples

**Example 1**
```text
Input: root = [3,9,20,null,null,15,7]
Output: true
```

**Example 2**
```text
Input: root = [1,2,2,3,3,null,null,4,4]
Output: false
```

**Example 3**
```text
Input: root = []
Output: true
```

## Constraints

- The number of nodes is in the range `[0, 5000]`
- `-10^4 <= Node.val <= 10^4`
