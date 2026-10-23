---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/count-good-nodes-in-binary-tree/
neetcode: https://neetcode.io/problems/count-good-nodes-in-binary-tree
---
# Count Good Nodes In Binary Tree

**Topic:** Trees · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) · [NeetCode](https://neetcode.io/problems/count-good-nodes-in-binary-tree)

## Problem

Given the `root` of a binary tree, a node `X` is called **good** if, on the path from the root down to `X`, no node has a value strictly greater than `X`'s value. Return the number of good nodes in the tree. (The root is always good.)

## Examples

**Example 1**
```text
Input: root = [3,1,4,3,null,1,5]
Output: 4
Explanation: the root 3, the 4, the 5, and the lower-left 3 are good.
```

**Example 2**
```text
Input: root = [3,3,null,4,2]
Output: 3
Explanation: node 2 is not good because 3 lies above it.
```

**Example 3**
```text
Input: root = [1]
Output: 1
```

## Constraints

- The number of nodes is in the range `[1, 10^5]`
- `-10^4 <= Node.val <= 10^4`
