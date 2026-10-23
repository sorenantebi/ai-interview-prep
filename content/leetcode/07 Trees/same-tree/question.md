---
topic: "Trees"
difficulty: Easy
leetcode: https://leetcode.com/problems/same-tree/
neetcode: https://neetcode.io/problems/same-binary-tree
---
# Same Tree

**Topic:** Trees · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/same-tree/) · [NeetCode](https://neetcode.io/problems/same-binary-tree)

## Problem

Given the roots `p` and `q` of two binary trees, return `true` if the trees are identical — same shape and equal values at every corresponding node — and `false` otherwise. Two empty trees are identical.

## Examples

**Example 1**
```text
Input: p = [1,2,3], q = [1,2,3]
Output: true
```

**Example 2**
```text
Input: p = [1,2], q = [1,null,2]
Output: false
```

**Example 3**
```text
Input: p = [1,2,1], q = [1,1,2]
Output: false
```

## Constraints

- The number of nodes in each tree is in the range `[0, 100]`
- `-10^4 <= Node.val <= 10^4`
