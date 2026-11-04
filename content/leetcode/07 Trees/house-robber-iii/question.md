---
video: https://www.youtube.com/watch?v=nHR8ytpzz7c
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/house-robber-iii/
neetcode: https://neetcode.io/problems/house-robber-iii
---
# House Robber III

**Topic:** Trees · **Difficulty:** Medium

## Problem

A thief has found a new area to rob. The only entrance is called `root`. Every house other than `root` has exactly one parent house, so all the houses form a binary tree.

If two directly-linked houses (a parent and one of its children) are broken into on the same night, the police are contacted automatically.

Given the `root` of the binary tree, where each node's value is the amount of money in that house, return the maximum amount of money the thief can rob without alerting the police.

## Examples

**Example 1**
```text
Input: root = [3,2,3,null,3,null,1]
Output: 7
```
Explanation: The maximum amount of money the thief can rob is 3 + 3 + 1 = 7.

**Example 2**
```text
Input: root = [3,4,5,1,3,null,1]
Output: 9
```
Explanation: The maximum amount of money the thief can rob is 4 + 5 = 9.

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `0 <= Node.val <= 10^4`
