---
topic: "PyTorch Tensors"
difficulty: Medium
---
# Scatter-Add Counts

**Topic:** PyTorch Tensors · **Difficulty:** Medium

## Problem

You have `N` embeddings `x` of shape `(N, D)` (float) and their class `labels` of shape `(N,)` (int64, values in `[0, num_classes)`). Compute each class's mean embedding (a "class prototype").

Return a tensor of shape `(num_classes, D)` whose row `c` is the mean of the rows of `x` labelled `c`. A class with no samples gets a row of zeros. Count and sum with scatter-style operations (`index_add_`, `scatter_add_`, `bincount`, …): no Python loops over samples or classes.

## Examples

**Example 1**
```text
Input: x = [[1.0, 2.0], [3.0, 4.0], [10.0, 0.0]], labels = [0, 0, 2], num_classes = 3
Output: [[2.00000,3.00000],[0.00000,0.00000],[10.00000,0.00000]]
Explanation: Class 1 has no samples, so its row is zeros.
```

**Example 2**
```text
Input: x = [[5.0], [7.0]], labels = [1, 1], num_classes = 2
Output: [[0.00000],[6.00000]]
```

## Constraints

- `1 <= N <= 10^5`, `1 <= D <= 256`, `1 <= num_classes <= 1000`
- `0 <= labels[i] < num_classes`
