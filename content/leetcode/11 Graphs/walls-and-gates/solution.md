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

## C++

```cpp
/*
    Given grid: -1 wall, 0 gate, INF empty, fill each empty w/ dist to nearest gate

    BFS traversal, shortest path from each gate to all empty rooms
    Each gate only looks at within 1 space, then next gate, guarantees shortest

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    void wallsAndGates(vector<vector<int>>& rooms) {
        int m = rooms.size();
        int n = rooms[0].size();
        
        queue<pair<int, int>> q;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (rooms[i][j] == 0) {
                    q.push({i, j});
                }
            }
        }
        
        while (!q.empty()) {
            int row = q.front().first;
            int col = q.front().second;
            q.pop();
            
            for (int i = 0; i < 4; i++) {
                int x = row + dirs[i][0];
                int y = col + dirs[i][1];
                
                if (x < 0 || x >= m || y < 0 || y >= n || rooms[x][y] != INT_MAX) {
                    continue;
                }
                
                rooms[x][y] = rooms[row][col] + 1;
                q.push({x, y});
            }
        }
    }
private:
    vector<vector<int>> dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
};
```
