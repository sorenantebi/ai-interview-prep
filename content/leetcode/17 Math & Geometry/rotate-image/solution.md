---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/rotate-image/
neetcode: https://neetcode.io/problems/rotate-matrix
---
# Rotate Image - Solution

**Question:** Rotate Image - Question · **Difficulty:** Medium

## Intuition

A 90-degree clockwise rotation is the same as transposing the matrix (reflecting it across the main diagonal) and then reversing each row (reflecting it horizontally). Each of those reflections is a set of simple in-place swaps, so no extra matrix is needed.

## Approach

1. **Transpose:** for every `i < j`, swap `matrix[i][j]` with `matrix[j][i]`.
2. **Reverse each row:** call `row.reverse()` on every row.

## Code

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        l, r = 0, len(matrix) - 1
        while l < r:
            for i in range(r - l):
                top, bottom = l, r

                # save the topleft
                topLeft = matrix[top][l + i]

                # move bottom left into top left
                matrix[top][l + i] = matrix[bottom - i][l]

                # move bottom right into bottom left
                matrix[bottom - i][l] = matrix[bottom][r - i]

                # move top right into bottom right
                matrix[bottom][r - i] = matrix[top + i][r]

                # move top left into top right
                matrix[top + i][r] = topLeft
            r -= 1
            l += 1
```

## Complexity

- **Time:** `O(n^2)`: each element is touched a constant number of times.
- **Space:** `O(1)`: only swaps are used.

## Other Approaches

- **Layer-by-layer four-way swap:** for each ring, rotate groups of four cells (top -> right -> bottom -> left) using one temporary variable. Time `O(n^2)`, Space `O(1)`.
- **Copy into a new matrix:** set `res[j][n-1-i] = matrix[i][j]` and copy back. This breaks the in-place requirement. Time `O(n^2)`, Space `O(n^2)`.

## Key Takeaway

A rotation can be built from two reflections. Clockwise is transpose then reverse each row; counter-clockwise is transpose then reverse the order of the rows (or reverse each row first, then transpose).
