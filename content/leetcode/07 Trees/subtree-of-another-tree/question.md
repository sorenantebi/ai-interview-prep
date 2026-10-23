---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/subtree-of-another-tree/
neetcode: https://neetcode.io/problems/subtree-of-a-binary-tree
---
# Subtree of Another Tree

**Topic:** Trees · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/subtree-of-another-tree/) · [NeetCode](https://neetcode.io/problems/subtree-of-a-binary-tree)

## Problem

Given the roots of two binary trees `root` and `subRoot`, return `true` if some node of `root` is the root of a subtree that is **identical** to `subRoot` (same structure and values), and `false` otherwise. A subtree of a node consists of that node and **all** of its descendants — so a partial match that leaves out some descendants does not count. The whole tree `root` is also considered a subtree of itself.

## Examples

**Example 1**
```text
Input: root = [3,4,5,1,2], subRoot = [4,1,2]
Output: true
```

**Example 2**
```text
Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
Output: false
Explanation: node 4 in root has an extra descendant 0.
```

## Constraints

- The number of nodes in `root` is in the range `[1, 2000]`
- The number of nodes in `subRoot` is in the range `[1, 1000]`
- `-10^4 <= Node.val <= 10^4`
