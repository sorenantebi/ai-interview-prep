---
video: https://www.youtube.com/watch?v=Cpg8f79luEA
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/insert-into-a-binary-search-tree/
neetcode: https://neetcode.io/problems/insert-into-a-binary-search-tree
---
# Insert into a Binary Search Tree

**Topic:** Trees · **Difficulty:** Medium

## Problem

You are given the root node of a binary search tree (BST) and a value to insert into it. Insert the value so that the tree remains a valid BST, and return the root of the resulting tree. The value is guaranteed not to already exist in the tree.

More than one valid result may exist, as long as the tree is still a BST after the insertion. Any of them is accepted.

## Examples

**Example 1**
```text
Input: root = [4,2,7,1,3], val = 5
Output: [4,2,7,1,3,5]
```

**Example 2**
```text
Input: root = [40,20,60,10,30,50,70], val = 25
Output: [40,20,60,10,30,50,70,null,null,25]
```

**Example 3**
```text
Input: root = [4,2,7,1,3,null,null,null,null,null,null], val = 5
Output: [4,2,7,1,3,5]
```

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-10^8 <= Node.val <= 10^8`
- All values `Node.val` are unique.
- `-10^8 <= val <= 10^8`
- It is guaranteed that `val` does not exist in the original BST.
