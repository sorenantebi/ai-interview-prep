---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/kth-smallest-element-in-a-bst/
neetcode: https://neetcode.io/problems/kth-smallest-integer-in-bst
---
# Kth Smallest Element In a Bst

**Topic:** Trees · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) · [NeetCode](https://neetcode.io/problems/kth-smallest-integer-in-bst)

## Problem

Given the `root` of a binary search tree and an integer `k`, return the `k`-th smallest value among all nodes (1-indexed).

Follow-up: if the BST is modified often (inserts/deletes) and you need the k-th smallest frequently, how would you optimize?

## Examples

**Example 1**
```text
Input: root = [3,1,4,null,2], k = 1
Output: 1
```

**Example 2**
```text
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
```

## Constraints

- The number of nodes is `n`, with `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`
