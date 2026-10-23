---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/merge-triplets-to-form-target-triplet/
neetcode: https://neetcode.io/problems/merge-triplets-to-form-target
---
# Merge Triplets to Form Target Triplet

**Topic:** Greedy · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) · [NeetCode](https://neetcode.io/problems/merge-triplets-to-form-target)

## Problem

A triplet is an array of three integers. You are given a 2-D array `triplets` where `triplets[i] = [a_i, b_i, c_i]`, and a target triplet `target = [x, y, z]`.

You may apply the following operation any number of times (including zero): choose two indices `i != j` and replace `triplets[j]` with `[max(a_i, a_j), max(b_i, b_j), max(c_i, c_j)]`.

Return `true` if it is possible for `target` to appear as an element of `triplets` after some sequence of operations, otherwise `false`.

## Examples

**Example 1**
```text
Input: triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
Output: true
Explanation: Merge [2,5,3] and [1,7,5] -> [2,7,5].
```

**Example 2**
```text
Input: triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
Output: false
```

**Example 3**
```text
Input: triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
Output: true
```

## Constraints

- `1 <= triplets.length <= 10^5`
- `triplets[i].length == target.length == 3`
- `1 <= a_i, b_i, c_i, x, y, z <= 1000`
