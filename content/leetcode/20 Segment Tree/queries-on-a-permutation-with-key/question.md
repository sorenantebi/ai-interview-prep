---
topic: "Segment Tree"
difficulty: Medium
leetcode: https://leetcode.com/problems/queries-on-a-permutation-with-key/
---
# Queries on a Permutation With Key

**Topic:** Segment Tree · **Difficulty:** Medium

## Problem

You are given an array `queries` of positive integers between `1` and `m`. Start with the permutation `P = [1, 2, 3, ..., m]`.

Process each `queries[i]` in order, from `i = 0` to `i = queries.length - 1`. For each one, find the position (0-indexed) of `queries[i]` in the current permutation `P`, record that position as the result for this query, and then move `queries[i]` to the front of `P`.

Return an array containing the result of every query.

## Examples

**Example 1**
```text
Input: queries = [3,1,2,1], m = 5
Output: [2,1,2,1]
```
Explanation: P = [1,2,3,4,5] → 3 is at index 2, P becomes [3,1,2,4,5]. Then 1 is at index 1, P becomes [1,3,2,4,5]. Then 2 is at index 2, P becomes [2,1,3,4,5]. Then 1 is at index 1, P becomes [1,2,3,4,5].

**Example 2**
```text
Input: queries = [4,1,2,2], m = 4
Output: [3,1,2,0]
```

**Example 3**
```text
Input: queries = [7,5,5,8,3], m = 8
Output: [6,5,0,7,5]
```

## Constraints

- `1 <= m <= 10^3`
- `1 <= queries.length <= m`
- `1 <= queries[i] <= m`
