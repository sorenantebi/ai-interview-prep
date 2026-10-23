---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/unique-paths/
neetcode: https://neetcode.io/problems/count-paths
---
# Unique Paths - Solution

**Question:** Unique Paths - Question · **Difficulty:** Medium

## Intuition

The only ways to enter cell `(r, c)` are from the cell above or the cell to the left, so `paths(r, c) = paths(r-1, c) + paths(r, c-1)`. Every cell in the first row or first column has exactly one path. Since each row depends only on the previous row, a single 1-D array is enough.

## Approach

1. Create `row = [1] * n` (the first row: one way to reach each cell).
2. For each subsequent row, sweep left to right: `row[c] += row[c-1]` — `row[c]` still holds the value from above, `row[c-1]` is the freshly updated left neighbour.
3. Return `row[-1]`.

## Code

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row = [1] * n

        for i in range(m - 1):
            newRow = [1] * n
            for j in range(n - 2, -1, -1):
                newRow[j] = newRow[j + 1] + row[j]
            row = newRow
        return row[0]

        # O(n * m) O(n)
```

## Complexity

- **Time:** `O(m * n)` — each cell is filled once.
- **Space:** `O(n)` — a single row is kept.

## Other Approaches

- **Combinatorics:** the path is a sequence of `m-1` downs and `n-1` rights, so the answer is `C(m+n-2, m-1)` — Time `O(min(m, n))`, Space `O(1)`.
- **Top-down memoized recursion:** recurse on `(r, c)` with a cache — Time `O(m * n)`, Space `O(m * n)`.

## Key Takeaway

Grid path-counting DP: value = sum of the predecessors' values; when only the previous row is needed, roll the DP into one array.
