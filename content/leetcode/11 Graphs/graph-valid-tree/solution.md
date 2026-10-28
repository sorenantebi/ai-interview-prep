---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/graph-valid-tree/
neetcode: https://neetcode.io/problems/valid-tree
---
# Graph Valid Tree - Solution

**Question:** Graph Valid Tree - Question · **Difficulty:** Medium

## Intuition

A graph on `n` nodes is a tree iff it has exactly `n - 1` edges **and** no cycle (equivalently, `n - 1` edges and connected). Check the edge count first, then use **Union-Find**: if an edge joins two nodes that already share a root, it closes a cycle.

## Approach

1. If `len(edges) != n - 1`, return `false` (too few → disconnected, too many → cycle).
2. Initialize Union-Find with `n` singleton sets.
3. For each edge `(a, b)`, find both roots; if they are equal, a cycle exists → return `false`. Otherwise union them.
4. With `n - 1` edges and no cycle, the graph is connected → return `true`.

## Code

```python
# Problem is free on Lintcode
class Solution:
    """
    @param n: An integer
    @param edges: a list of undirected edges
    @return: true if it's a valid tree, or false
    """

    def validTree(self, n, edges):
        if not n:
            return True
        adj = {i: [] for i in range(n)}
        for n1, n2 in edges:
            adj[n1].append(n2)
            adj[n2].append(n1)

        visit = set()

        def dfs(i, prev):
            if i in visit:
                return False

            visit.add(i)
            for j in adj[i]:
                if j == prev:
                    continue
                if not dfs(j, i):
                    return False
            return True

        return dfs(0, -1) and n == len(visit)
    
    
    
    # alternative solution via DSU O(ElogV) time complexity and 
    # save some space as we don't recreate graph\tree into adjacency list prior dfs and loop over the edge list directly
    class Solution:
    """
    @param n: An integer
    @param edges: a list of undirected edges
    @return: true if it's a valid tree, or false
    """
    def __find(self, n: int) -> int:
        while n != self.parents.get(n, n):
            n = self.parents.get(n, n)
        return n

    def __connect(self, n: int, m: int) -> None:
        pn = self.__find(n)
        pm = self.__find(m)
        if pn == pm:
            return
        if self.heights.get(pn, 1) > self.heights.get(pm, 1):
            self.parents[pn] = pm
        else:
            self.parents[pm] = pn
            self.heights[pm] = self.heights.get(pn, 1) + 1
        self.components -= 1

    def valid_tree(self, n: int, edges: List[List[int]]) -> bool:
        # init here as not sure that ctor will be re-invoked in different tests
        self.parents = {}
        self.heights = {}
        self.components = n

        for e1, e2 in edges:
            if self.__find(e1) == self.__find(e2):  # 'redundant' edge
                return False
            self.__connect(e1, e2)

        return self.components == 1  # forest contains one tree
```

## Complexity

- **Time:** `O(n + E * α(n))` — near-constant time per union/find.
- **Space:** `O(n)` — parent and rank arrays.

## Other Approaches

- **DFS/BFS:** after the `n - 1` edge check, traverse from node 0 and verify all `n` nodes are visited — Time `O(n + E)`, Space `O(n + E)` for the adjacency list.

## Key Takeaway

Tree ⇔ `n - 1` edges + connected ⇔ `n - 1` edges + acyclic; Union-Find is the go-to tool for cycle detection in undirected graphs.

## C++

```cpp
/*
    Graph of nodes, list of edges, determine if edges make valid tree
    Ex. n = 5, edges = [[0,1],[0,2],[0,3],[1,4]] -> true

    (1) For graph to be a valid tree, must have exactly n - 1 edges
    (2) If graph fully connected & has n - 1 edges, can't contain cycle

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    bool validTree(int n, vector<vector<int>>& edges) {
        vector<vector<int>> adj(n);
        for (int i = 0; i < edges.size(); i++) {
            vector<int> edge = edges[i];
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }
        
        vector<bool> visited(n);
        if (hasCycle(adj, visited, -1, 0)) {
            return false;
        }
        
        for (int i = 0; i < visited.size(); i++) {
            if (!visited[i]) {
                return false;
            }
        }
        return true;
    }
private:
    bool hasCycle(vector<vector<int>>& adj, vector<bool>& visited, int parent, int child) {
        if (visited[child]) {
            return true;
        }
        visited[child] = true;
        // checking for cycles and connectedness
        for (int i = 0; i < adj[child].size(); i++) {
            int curr = adj[child][i];
            if (curr != parent && hasCycle(adj, visited, child, curr)) {
                return true;
            }
        }
        return false;
    }
};
```
