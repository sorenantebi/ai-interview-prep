---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/course-schedule-iv/
neetcode: https://neetcode.io/problems/course-schedule-iv
---
# Course Schedule IV - Solution

## Intuition

A query asks whether `v` is reachable from `u` in a directed graph. With at most 100 nodes but up to 10^4 queries, it pays to precompute reachability between all pairs once, so each query becomes an O(1) lookup.

## Approach

1. Build an `n x n` boolean matrix `reach`, where `reach[a][b]` is true if `a` is a prerequisite of `b`.
2. Mark every direct prerequisite pair `[a, b]` as `reach[a][b] = True`.
3. Run the Floyd–Warshall transitive closure: for each intermediate course `k`, for each `i` and `j`, set `reach[i][j] |= reach[i][k] and reach[k][j]`.
4. Answer each query `[u, v]` by returning `reach[u][v]`.

## Code

```python
class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        adj = defaultdict(list)
        for prereq, crs in prerequisites:
            adj[crs].append(prereq)
        
        def dfs(crs):
            if crs not in prereqMap:
                prereqMap[crs] = set()
                for pre in adj[crs]:
                    prereqMap[crs] |= dfs(pre)
            prereqMap[crs].add(crs)
            return prereqMap[crs]

        prereqMap = {} # map course -> set indirect prereqs
        for crs in range(numCourses):
            dfs(crs)

        res = []
        for u, v in queries:
            res.append(u in prereqMap[v])
        return res
```

## Complexity

- **Time:** `O(n^3 + q)` — the closure triple loop over `n` courses, plus one O(1) lookup per query.
- **Space:** `O(n^2)` — the reachability matrix.

## Other Approaches

- **DFS/BFS from each node:** compute the set of reachable nodes from every course, then answer queries by lookup — Time `O(n * (n + e) + q)` / Space `O(n^2)`
- **Topological sort with ancestor sets:** process courses in topological order (Kahn's algorithm), propagating each course's prerequisite set to its successors — Time `O(n * (n + e) + q)` / Space `O(n^2)`
- **Per-query BFS/DFS:** run a search for each query without precomputation — Time `O(q * (n + e))` / Space `O(n + e)`
