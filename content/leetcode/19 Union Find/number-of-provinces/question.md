---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-provinces/
---
# Number of Provinces

**Topic:** Union Find · **Difficulty:** Medium

## Problem

There are `n` cities, some of which are connected and some of which are not. If city `a` is directly connected to city `b`, and city `b` is directly connected to city `c`, then city `a` is indirectly connected to city `c`.

A province is a group of cities that are directly or indirectly connected to each other, with no other cities outside the group connected to it.

You are given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the `i`-th city and the `j`-th city are directly connected, and `isConnected[i][j] = 0` otherwise.

Return the total number of provinces.

## Examples

**Example 1**
```text
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2
```

**Example 2**
```text
Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
```

## Constraints

- `1 <= n <= 200`
- `n == isConnected.length`
- `n == isConnected[i].length`
- `isConnected[i][j]` is `1` or `0`
- `isConnected[i][i] == 1`
- `isConnected[i][j] == isConnected[j][i]`
