---
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/transpose-matrix/
neetcode: https://neetcode.io/problems/transpose-matrix
---
# Transpose Matrix - Solution

## Intuition

Transposing swaps rows and columns: an `m x n` matrix becomes `n x m`, and `result[j][i] = matrix[i][j]`. Because the matrix may be non-square, an in-place swap is not possible in general, so we build a new matrix.

## Approach

1. Read the dimensions `m` (rows) and `n` (columns).
2. Allocate a result with `n` rows and `m` columns.
3. For every `(i, j)`, set `result[j][i] = matrix[i][j]`.
4. Return the result.

## Code

```python
from typing import List, Optional

class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        m, n = len(matrix), len(matrix[0])
        res = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                res[j][i] = matrix[i][j]
        return res
```

## Complexity

- **Time:** `O(m * n)` — every element is visited exactly once.
- **Space:** `O(m * n)` — the output matrix holds all elements (the output is required, so no extra auxiliary space is used).

## Other Approaches

- **zip(*matrix):** Python one-liner `[list(r) for r in zip(*matrix)]` that groups the i-th elements of every row — Time `O(m * n)` / Space `O(m * n)`
- **In-place swap (square only):** swap `matrix[i][j]` with `matrix[j][i]` for `j > i`; not applicable to non-square input — Time `O(n^2)` / Space `O(1)`
