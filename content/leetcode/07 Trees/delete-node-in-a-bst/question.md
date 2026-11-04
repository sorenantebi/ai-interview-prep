---
video: https://www.youtube.com/watch?v=LFzAoJJt92M
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/delete-node-in-a-bst/
neetcode: https://neetcode.io/problems/delete-node-in-a-bst
---
# Delete Node in a BST

**Topic:** Trees · **Difficulty:** Medium

## Problem

You are given the root of a binary search tree (BST) and an integer `key`. Delete the node whose value equals `key` from the BST, and return the root of the resulting BST (the root may change).

Deletion has two stages:

1. Search for the node to remove.
2. If the node is found, delete it.

The result must still be a valid BST. More than one valid result can exist; any of them is accepted.

**Follow up:** Can you solve it in `O(height of tree)` time?

## Examples

**Example 1**
```text
Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7]
```
The node with value 3 is found and deleted. Another valid answer is `[5,2,6,null,4,null,7]`, which is also accepted.

**Example 2**
```text
Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
```
The tree contains no node with value 0, so it is unchanged.

**Example 3**
```text
Input: root = [], key = 0
Output: []
```

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- Each node has a unique value.
- `root` is a valid binary search tree.
- `-10^5 <= key <= 10^5`
