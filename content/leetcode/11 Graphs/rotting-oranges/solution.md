---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/rotting-oranges/
neetcode: https://neetcode.io/problems/rotting-fruit
---
# Rotting Oranges - Solution

**Question:** Rotting Oranges - Question · **Difficulty:** Medium

## Intuition

Rot spreads from all rotten oranges simultaneously, one step per minute — exactly the layer-by-layer expansion of a **multi-source BFS**. The number of BFS levels needed to reach every fresh orange is the answer; if any fresh orange is left unreached, return `-1`.

## Approach

1. Scan the grid: enqueue all rotten oranges and count fresh ones.
2. While the queue is non-empty and fresh oranges remain:
   - Process exactly the current level (all oranges that rotted in the previous minute).
   - Rot each fresh neighbor, decrement the fresh count, enqueue it.
   - Increment `minutes` after the level.
3. Return `minutes` if `fresh == 0`, else `-1`.

## Code

```python
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        q = collections.deque()
        fresh = 0
        time = 0

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 1:
                    fresh += 1
                if grid[r][c] == 2:
                    q.append((r, c))

        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        while fresh > 0 and q:
            length = len(q)
            for i in range(length):
                r, c = q.popleft()

                for dr, dc in directions:
                    row, col = r + dr, c + dc
                    # if in bounds and nonrotten, make rotten
                    # and add to q
                    if (
                        row in range(len(grid))
                        and col in range(len(grid[0]))
                        and grid[row][col] == 1
                    ):
                        grid[row][col] = 2
                        q.append((row, col))
                        fresh -= 1
            time += 1
        return time if fresh == 0 else -1
```

## Complexity

- **Time:** `O(m * n)` — each cell is enqueued at most once.
- **Space:** `O(m * n)` — the BFS queue.

## Other Approaches

- **Repeated simulation:** each minute scan the whole grid and rot neighbors of rotten cells until nothing changes — Time `O((m * n)^2)`, Space `O(m * n)` for the next-state copy.

## Key Takeaway

Simultaneous spreading over time = multi-source BFS processed level by level; track a "remaining" counter to detect unreachable targets.
