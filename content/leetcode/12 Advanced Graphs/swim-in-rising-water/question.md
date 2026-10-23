---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/swim-in-rising-water/
neetcode: https://neetcode.io/problems/swim-in-rising-water
---
# Swim In Rising Water

**Topic:** Advanced Graphs · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/swim-in-rising-water/) · [NeetCode](https://neetcode.io/problems/swim-in-rising-water)

## Problem

You are given an `n x n` grid where `grid[r][c]` is the elevation of cell `(r, c)`; the values are a permutation of `0 .. n^2 - 1`. Rain starts falling, and at time `t` the water level everywhere is `t`.

You may swim from a cell to a 4-directionally adjacent cell only if both cells have elevation at most `t`. Swimming any distance takes zero time. Starting at `(0, 0)`, return the smallest time `t` at which you can reach `(n - 1, n - 1)`.

## Examples

**Example 1**
```text
Input: grid = [[0,2],[1,3]]
Output: 3
Explanation: The target cell itself has elevation 3, so you must wait until t = 3.
```

**Example 2**
```text
Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
Output: 16
```

**Example 3**
```text
Input: grid = [[0]]
Output: 0
```

## Constraints

- `n == grid.length == grid[i].length`
- `1 <= n <= 50`
- `0 <= grid[i][j] < n^2`
- All values in `grid` are distinct.
