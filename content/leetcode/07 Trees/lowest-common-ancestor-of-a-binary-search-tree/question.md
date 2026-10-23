---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
neetcode: https://neetcode.io/problems/lowest-common-ancestor-in-binary-search-tree
---
# Lowest Common Ancestor of a Binary Search Tree

**Topic:** Trees · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) · [NeetCode](https://neetcode.io/problems/lowest-common-ancestor-in-binary-search-tree)

## Problem

You are given the `root` of a **binary search tree** and two nodes `p` and `q` that are guaranteed to exist in it. Return their **lowest common ancestor (LCA)**: the deepest node that has both `p` and `q` as descendants, where a node counts as a descendant of itself (so if `p` is an ancestor of `q`, the answer is `p`). All values in the BST are unique and `p != q`.

## Examples

**Example 1**
```text
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
```

**Example 2**
```text
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
Output: 2
Explanation: a node may be its own ancestor.
```

**Example 3**
```text
Input: root = [2,1], p = 2, q = 1
Output: 2
```

## Constraints

- The number of nodes is in the range `[2, 10^5]`
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique; `p != q`; both exist in the BST
