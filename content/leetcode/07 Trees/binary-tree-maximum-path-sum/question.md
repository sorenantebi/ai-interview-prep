---
topic: "Trees"
difficulty: Hard
leetcode: https://leetcode.com/problems/binary-tree-maximum-path-sum/
neetcode: https://neetcode.io/problems/binary-tree-maximum-path-sum
---
# Binary Tree Maximum Path Sum

**Topic:** Trees · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/binary-tree-maximum-path-sum/) · [NeetCode](https://neetcode.io/problems/binary-tree-maximum-path-sum)

## Problem

A **path** in a binary tree is a sequence of nodes in which every consecutive pair is joined by an edge; each node appears at most once, and the path need not pass through the root. A path must contain **at least one** node. The path sum is the sum of its node values. Given the `root`, return the maximum path sum over all non-empty paths. Node values can be negative.

## Examples

**Example 1**
```text
Input: root = [1,2,3]
Output: 6
Explanation: path 2 -> 1 -> 3.
```

**Example 2**
```text
Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: path 15 -> 20 -> 7.
```

**Example 3**
```text
Input: root = [-3]
Output: -3
```

## Constraints

- The number of nodes is in the range `[1, 3 * 10^4]`
- `-1000 <= Node.val <= 1000`
