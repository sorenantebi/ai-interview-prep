---
topic: "ML From Scratch"
difficulty: Medium
---
# K-Means

**Topic:** ML From Scratch · **Difficulty:** Medium

## Problem

Run Lloyd's k-means algorithm from given starting centroids.

`X` has shape `(n, d)` and `centroids` has shape `(k, d)`. Repeat the following `iterations` times:

1. **Assign:** give each point the label of its nearest centroid by Euclidean distance. If a point is equally close to several centroids, pick the one with the smallest index.
2. **Update:** move each centroid to the mean of the points assigned to it. A centroid with no assigned points stays where it is.

Return `[centroids, labels]`: the centroids after the last update (float array of shape `(k, d)`) and the labels from the last assign step (integer array of shape `(n,)`). Don't use Python loops over the points.

## Examples

**Example 1**
```text
Input: X = [[0.0, 0.0], [0.0, 1.0], [10.0, 10.0], [10.0, 11.0]], centroids = [[0.0, 0.0], [10.0, 10.0]], iterations = 1
Output: [[[0.00000,0.50000],[10.00000,10.50000]],[0,0,1,1]]
```

**Example 2**
```text
Input: X = [[1.0], [2.0], [9.0], [12.0]], centroids = [[0.0], [5.0], [100.0]], iterations = 2
Output: [[[1.50000],[10.50000],[100.00000]],[0,0,1,1]]
```

## Constraints

- `1 <= n <= 10^4`
- `1 <= k <= 50`
- `1 <= d <= 20`
- `1 <= iterations <= 100`
