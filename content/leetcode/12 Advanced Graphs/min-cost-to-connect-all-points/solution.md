---
topic: "Advanced Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/min-cost-to-connect-all-points/
neetcode: https://neetcode.io/problems/min-cost-to-connect-points
---
# Min Cost to Connect All Points - Solution

**Question:** Min Cost to Connect All Points - Question · **Difficulty:** Medium

## Intuition

We need a minimum spanning tree of a complete graph where every pair of points is an edge. Because the graph is dense (`~n^2/2` edges), the array-based version of **Prim's algorithm** is ideal: it runs in `O(n^2)` without ever materialising the edges or using a heap.

## Approach

1. Keep `min_dist[i]` = cheapest known edge connecting point `i` to the growing tree (start: `inf`, and `0` for point 0).
2. Repeat `n` times: pick the unvisited point with the smallest `min_dist`, add that cost to the total, and mark it visited.
3. Relax: for every unvisited point `j`, set `min_dist[j] = min(min_dist[j], manhattan(cur, j))`.
4. Return the total.

## Code

```python
class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        N = len(points)
        adj = {i: [] for i in range(N)}  # i : list of [cost, node]
        for i in range(N):
            x1, y1 = points[i]
            for j in range(i + 1, N):
                x2, y2 = points[j]
                dist = abs(x1 - x2) + abs(y1 - y2)
                adj[i].append([dist, j])
                adj[j].append([dist, i])

        # Prim's
        res = 0
        visit = set()
        minH = [[0, 0]]  # [cost, point]
        while len(visit) < N:
            cost, i = heapq.heappop(minH)
            if i in visit:
                continue
            res += cost
            visit.add(i)
            for neiCost, nei in adj[i]:
                if nei not in visit:
                    heapq.heappush(minH, [neiCost, nei])
        return res
```

## Complexity

- **Time:** `O(n^2)` — `n` rounds, each scanning all points.
- **Space:** `O(n)` — the `min_dist` and `in_tree` arrays.

## Other Approaches

- **Kruskal + Union-Find:** generate all `n^2/2` edges, sort, union greedily — Time `O(n^2 log n)`, Space `O(n^2)`.
- **Prim with a heap:** lazy heap of `(cost, point)` — Time `O(n^2 log n)`, Space `O(n^2)` (worse than array Prim on dense graphs).

## Key Takeaway

For MST on a dense/complete graph, array-based Prim (`O(V^2)`) beats heap-based Prim and Kruskal; for sparse graphs prefer Kruskal or heap Prim.

## C++

```cpp
/*
    Given array of points, return min cost to connect all points
    All points have 1 path b/w them, cost is Manhattan distance

    MST problem, Prim's, greedily pick node not in MST & has smallest edge cost
    Add to MST, & for all its neighbors, try to update min dist values, repeat

    Time: O(n^2)
    Space: O(n)
*/

class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size();
        
        int edgesUsed = 0;
        // track visited nodes
        vector<bool> inMST(n);
        vector<int> minDist(n, INT_MAX);
        minDist[0] = 0;
        
        int result = 0;
        
        while (edgesUsed < n) {
            int currMinEdge = INT_MAX;
            int currNode = -1;
            
            // greedily pick lowest cost node not in MST
            for (int i = 0; i < n; i++) {
                if (!inMST[i] && currMinEdge > minDist[i]) {
                    currMinEdge = minDist[i];
                    currNode = i;
                }
            }
            
            result += currMinEdge;
            edgesUsed++;
            inMST[currNode] = true;
            
            // update adj nodes of curr node
            for (int i = 0; i < n; i++) {
                int cost = abs(points[currNode][0] - points[i][0])
                    + abs(points[currNode][1] - points[i][1]);
                
                if (!inMST[i] && minDist[i] > cost) {
                    minDist[i] = cost;
                }
            }
        }
        
        return result;
    }
};
```
