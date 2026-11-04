---
video: https://www.youtube.com/watch?v=UQ-1sBMV0v4
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/construct-quad-tree/
neetcode: https://neetcode.io/problems/construct-quad-tree
---
# Construct Quad Tree

**Topic:** Trees · **Difficulty:** Medium

## Problem

You are given an `n x n` matrix `grid` containing only `0`s and `1`s. Represent the grid as a Quad-Tree and return its root.

A Quad-Tree is a tree in which every internal node has exactly four children. Each node has two attributes:

- `val`: `True` if the node represents a region of all `1`s, `False` if it represents a region of all `0`s. When `isLeaf` is `False`, `val` may be either `True` or `False`; both are accepted.
- `isLeaf`: `True` if the node is a leaf, `False` if it has four children.

```text
class Node {
    public boolean val;
    public boolean isLeaf;
    public Node topLeft;
    public Node topRight;
    public Node bottomLeft;
    public Node bottomRight;
}
```

Build the tree as follows:

1. If the current region contains a single value (all `1`s or all `0`s), create a leaf node with `isLeaf = True`, `val` set to that value, and all four children `null`. Stop.
2. Otherwise, set `isLeaf = False`, set `val` to any value, and split the region into four equal sub-regions (top-left, top-right, bottom-left, bottom-right).
3. Recurse on each sub-region to build the corresponding child.

The expected output is the Quad-Tree serialized in level order, similar to binary tree serialization, where each node is written as `[isLeaf, val]` (with `True` written as `1` and `False` as `0`) and `null` marks a missing node below a leaf.

## Examples

**Example 1**
```text
Input: grid = [[0,1],[1,0]]
Output: [[0,1],[1,0],[1,1],[1,1],[1,0]]
```
The grid has mixed values, so the root is an internal node with four leaf children: top-left `0`, top-right `1`, bottom-left `1`, bottom-right `0`.

**Example 2**
```text
Input: grid = [[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0]]
Output: [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,[1,0],[1,0],[1,1],[1,1]]
```
The grid is not uniform, so it is split into four quadrants. The top-left, bottom-left and bottom-right quadrants are uniform. The top-right quadrant is mixed, so it is split again into four uniform sub-quadrants.

## Constraints

- `n == grid.length == grid[i].length`
- `n == 2^x` where `0 <= x <= 6`
- `grid[i][j]` is either `0` or `1`
