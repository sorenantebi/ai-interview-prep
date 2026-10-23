---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/validate-binary-search-tree/
neetcode: https://neetcode.io/problems/valid-binary-search-tree
---
# Validate Binary Search Tree

**Topic:** Trees · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/validate-binary-search-tree/) · [NeetCode](https://neetcode.io/problems/valid-binary-search-tree)

## Problem

Given the `root` of a binary tree, decide whether it is a valid **binary search tree**:

- every value in a node's left subtree is **strictly less** than the node's value,
- every value in a node's right subtree is **strictly greater** than the node's value,
- and both subtrees are themselves valid BSTs.

Return `true` or `false`. Duplicates make the tree invalid.

## Examples

**Example 1**
```text
Input: root = [2,1,3]
Output: true
```

**Example 2**
```text
Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: the right child 4 is smaller than the root 5.
```

**Example 3**
```text
Input: root = [5,4,6,null,null,3,7]
Output: false
Explanation: 3 sits in 5's right subtree, even though it is a valid left child of 6.
```

## Constraints

- The number of nodes is in the range `[1, 10^4]`
- `-2^31 <= Node.val <= 2^31 - 1`
