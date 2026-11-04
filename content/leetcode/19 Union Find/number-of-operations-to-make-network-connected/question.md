---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-operations-to-make-network-connected/
---
# Number of Operations to Make Network Connected

**Topic:** Union Find · **Difficulty:** Medium

## Problem

There are `n` computers numbered from `0` to `n - 1`, linked by ethernet cables. The array `connections` describes the network, where `connections[i] = [ai, bi]` is a cable directly joining computers `ai` and `bi`. Initially, any computer can reach any other computer, directly or indirectly, through the network.

You may take a cable out from between two directly connected computers and re-plug it between any pair of computers that are not yet directly connected. Each such move counts as one operation.

Return the minimum number of operations needed so that all computers end up connected. If it is impossible, return `-1`.

## Examples

**Example 1**
```text
Input: n = 4, connections = [[0,1],[0,2],[1,2]]
Output: 1
```
Remove the cable between computers 1 and 2 and place it between computers 1 and 3.

**Example 2**
```text
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
Output: 2
```

**Example 3**
```text
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
Output: -1
```
There are not enough cables.

## Constraints

- `1 <= n <= 10^5`
- `1 <= connections.length <= min(n * (n - 1) / 2, 10^5)`
- `connections[i].length == 2`
- `0 <= ai, bi < n`
- `ai != bi`
- There are no repeated connections.
- No two computers are connected by more than one cable.
