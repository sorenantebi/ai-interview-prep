---
video: https://www.youtube.com/watch?v=FqAoYAwbwV8
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/delete-leaves-with-a-given-value/
neetcode: https://neetcode.io/problems/delete-leaves-with-a-given-value
---
# Delete Leaves With a Given Value

**Topic:** Trees · **Difficulty:** Medium

## Problem

You are given the `root` of a binary tree and an integer `target`. Delete every leaf node whose value equals `target`.

Deleting a leaf may turn its parent into a new leaf. If that parent's value equals `target`, it must be deleted as well. Keep repeating this until no leaf with value `target` remains.

Return the root of the resulting tree (which may be `None` if every node is removed).

## Examples

**Example 1**
```text
Input: root = [1,2,3,2,null,2,4], target = 2
Output: [1,null,3,null,4]
```
Leaves with value 2 are removed first. Afterwards, the node with value 2 that was their parent becomes a leaf and is removed too.

**Example 2**
```text
Input: root = [1,3,3,3,2], target = 3
Output: [1,3,null,null,2]
```

**Example 3**
```text
Input: root = [1,2,null,2,null,2], target = 2
Output: [1]
```
Leaves with value 2 are removed at each step, one level at a time, until only the root remains.

## Constraints

- The number of nodes in the tree is in the range `[1, 3000]`.
- `1 <= Node.val, target <= 1000`
