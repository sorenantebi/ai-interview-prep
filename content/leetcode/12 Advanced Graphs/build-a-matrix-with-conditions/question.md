---
video: https://www.youtube.com/watch?v=khTKB1PzCuw
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/build-a-matrix-with-conditions/
neetcode: https://neetcode.io/problems/build-a-matrix-with-conditions
---
# Build a Matrix With Conditions

**Topic:** Advanced Graphs · **Difficulty:** Hard

## Problem

You are given a positive integer `k`, along with two 2D integer arrays: `rowConditions` of size `n`, where `rowConditions[i] = [above_i, below_i]`, and `colConditions` of size `m`, where `colConditions[i] = [left_i, right_i]`. All values in both arrays are between `1` and `k`.

Build a `k x k` matrix that contains each number from `1` to `k` exactly once, with every other cell set to `0`. The matrix must satisfy:

- For every `i`, the number `above_i` appears in a row strictly above the row containing `below_i`.
- For every `i`, the number `left_i` appears in a column strictly to the left of the column containing `right_i`.

Return any matrix that satisfies all the conditions. If no such matrix exists, return an empty matrix.

## Examples

**Example 1**
```text
Input: k = 3, rowConditions = [[1,2],[3,2]], colConditions = [[2,1],[3,2]]
Output: [[3,0,0],[0,0,1],[0,2,0]]
```
Number 1 is in row 1 and 2 is in row 2, so 1 is above 2. Number 3 is in row 0 and 2 is in row 2, so 3 is above 2. Number 2 is in column 1 and 1 is in column 2, so 2 is left of 1. Number 3 is in column 0 and 2 is in column 1, so 3 is left of 2. Multiple valid answers may exist.

**Example 2**
```text
Input: k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]
Output: []
```
The first two row conditions force 3 to be below 1, but the third requires 3 to be above 1. No matrix can satisfy all conditions, so the result is empty.

## Constraints

- `2 <= k <= 400`
- `1 <= rowConditions.length, colConditions.length <= 10^4`
- `rowConditions[i].length == colConditions[i].length == 2`
- `1 <= above_i, below_i, left_i, right_i <= k`
- `above_i != below_i`
- `left_i != right_i`
