---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/diameter-of-binary-tree/
neetcode: https://neetcode.io/problems/binary-tree-diameter
---
# Diameter of Binary Tree

**Topic:** Trees · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/diameter-of-binary-tree/) · [NeetCode](https://neetcode.io/problems/binary-tree-diameter)

## Problem

Given the `root` of a binary tree, return the length of its **diameter**: the longest path (measured in **edges**) between any two nodes. The path does not have to pass through the root.

## Examples

**Example 1**
```text
Input: root = [1,2,3,4,5]
Output: 3
Explanation: path 4 -> 2 -> 1 -> 3 (or 5 -> 2 -> 1 -> 3) has 3 edges.
```

**Example 2**
```text
Input: root = [1,2]
Output: 1
```

## Constraints

- The number of nodes is in the range `[1, 10^4]`
- `-100 <= Node.val <= 100`
