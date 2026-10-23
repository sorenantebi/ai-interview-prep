---
topic: "Trees"
difficulty: Hard
leetcode: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
neetcode: https://neetcode.io/problems/serialize-and-deserialize-binary-tree
---
# Serialize And Deserialize Binary Tree

**Topic:** Trees · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) · [NeetCode](https://neetcode.io/problems/serialize-and-deserialize-binary-tree)

## Problem

Design an algorithm to **serialize** a binary tree into a string and **deserialize** that string back into the original tree structure. Implement the `Codec` class:

- `serialize(root)` — encodes the tree as a single string.
- `deserialize(data)` — decodes a string produced by `serialize` and returns the root of an identical tree.

There are no restrictions on the string format; the only requirement is that `deserialize(serialize(root))` reproduces the same tree (structure and values). Values may be negative and the tree may be empty.

## Examples

**Example 1**
```text
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
```

**Example 2**
```text
Input: root = []
Output: []
```

## Constraints

- The number of nodes is in the range `[0, 10^4]`
- `-1000 <= Node.val <= 1000`
