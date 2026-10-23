---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/walls-and-gates/
neetcode: https://neetcode.io/problems/islands-and-treasure
---
# Walls And Gates - Solution

**Question:** Walls And Gates - Question · **Difficulty:** Medium

## Intuition

We want, for every room, the shortest distance to *any* gate. Running a BFS from each room (or each gate separately) repeats work. Instead, do a **multi-source BFS**: start with all gates in the queue at distance 0. BFS expands in rings of increasing distance, so the first time a room is reached is via its nearest gate.

## Approach

1. Enqueue the coordinates of every gate (`0`).
2. Pop a cell `(r, c)`; for each 4-directional neighbor that is an empty room (`INF`), set it to `rooms[r][c] + 1` and enqueue it.
3. Walls (`-1`), gates, and already-filled rooms are never `INF`, so they are skipped automatically — the grid doubles as the visited set.
4. Rooms never reached remain `INF`.

## Code

```python
class Solution:
    """
    @param rooms: m x n 2D grid
    @return: nothing
    """

    def walls_and_gates(self, rooms: List[List[int]]):
        ROWS, COLS = len(rooms), len(rooms[0])
        visit = set()
        q = deque()

        def addRooms(r, c):
            if (
                min(r, c) < 0
                or r == ROWS
                or c == COLS
                or (r, c) in visit
                or rooms[r][c] == -1
            ):
                return
            visit.add((r, c))
            q.append([r, c])

        for r in range(ROWS):
            for c in range(COLS):
                if rooms[r][c] == 0:
                    q.append([r, c])
                    visit.add((r, c))

        dist = 0
        while q:
            for i in range(len(q)):
                r, c = q.popleft()
                rooms[r][c] = dist
                addRooms(r + 1, c)
                addRooms(r - 1, c)
                addRooms(r, c + 1)
                addRooms(r, c - 1)
            dist += 1
```

## Complexity

- **Time:** `O(m * n)` — every cell is enqueued at most once.
- **Space:** `O(m * n)` — the BFS queue in the worst case.

## Other Approaches

- **BFS/DFS from each gate separately:** relax distances with `min` from every gate — Time `O(k * m * n)` for `k` gates, Space `O(m * n)`.
- **BFS from each empty room:** search outward until a gate is found — Time `O((m * n)^2)`, Space `O(m * n)`.

## Key Takeaway

"Distance to the nearest of many sources" → multi-source BFS: seed the queue with all sources at once.
