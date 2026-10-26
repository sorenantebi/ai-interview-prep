---
topic: "ML From Scratch"
difficulty: Easy
---
# K-Fold Indices

**Topic:** ML From Scratch · **Difficulty:** Easy

## Problem

Split the sample indices `0 .. n - 1` into `k` folds for cross-validation, without shuffling.

The validation sets are consecutive blocks in order: fold 0 takes the first block, fold 1 the next, and so on. Each fold has `n // k` indices, except that the first `n % k` folds get one extra index each.

Return a list of `k` pairs `[train, val]`, one per fold in order, where `val` is that fold's block and `train` is every other index. Both are lists of ints in increasing order.

## Examples

**Example 1**
```text
Input: n = 5, k = 2
Output: [[[3,4],[0,1,2]],[[0,1,2],[3,4]]]
```

**Example 2**
```text
Input: n = 7, k = 3
Output: [[[3,4,5,6],[0,1,2]],[[0,1,2,5,6],[3,4]],[[0,1,2,3,4],[5,6]]]
```

## Constraints

- `1 <= k <= n <= 10^5`
