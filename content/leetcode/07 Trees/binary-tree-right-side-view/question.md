---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/binary-tree-right-side-view/
neetcode: https://neetcode.io/problems/binary-tree-right-side-view
---
# Binary Tree Right Side View

**Topic:** Trees · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/binary-tree-right-side-view/) · [NeetCode](https://neetcode.io/problems/binary-tree-right-side-view)

## Problem

Imagine standing to the right of a binary tree. Given its `root`, return the values of the nodes you can see, ordered from top to bottom — i.e. the **rightmost** node of every level. An empty tree yields `[]`.

## Examples

**Example 1**
```text
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]
```

**Example 2**
```text
Input: root = [1,2,3,4,null,null,null,5]
Output: [1,3,4,5]
Explanation: the deepest node 5 sits under the left subtree but is still visible.
```

**Example 3**
```text
Input: root = [1,null,3]
Output: [1,3]
```

## Constraints

- The number of nodes is in the range `[0, 100]`
- `-100 <= Node.val <= 100`
