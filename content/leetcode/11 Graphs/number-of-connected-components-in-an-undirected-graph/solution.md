---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/
neetcode: https://neetcode.io/problems/count-connected-components
---
# Number of Connected Components In An Undirected Graph - Solution

**Question:** Number of Connected Components In An Undirected Graph - Question · **Difficulty:** Medium

## Intuition

Start by assuming every node is its own component (`n` components). Each edge that connects two **different** components merges them, reducing the count by one; edges inside a component change nothing. **Union-Find** tracks exactly this.

## Approach

1. Initialize `parent[i] = i` and `components = n`.
2. For each edge `(a, b)`, find both roots.
3. If the roots differ, union them (by size) and decrement `components`.
4. Return `components`.

## Code

```python
class UnionFind:
    def __init__(self):
        self.f = {}

    def findParent(self, x):
        y = self.f.get(x, x)
        if x != y:
            y = self.f[x] = self.findParent(y)
        return y

    def union(self, x, y):
        self.f[self.findParent(x)] = self.findParent(y)


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        dsu = UnionFind()
        for a, b in edges:
            dsu.union(a, b)
        return len(set(dsu.findParent(x) for x in range(n)))
```

## Complexity

- **Time:** `O(n + E * α(n))` — near-constant amortized union/find.
- **Space:** `O(n)` — parent and size arrays.

## Other Approaches

- **DFS/BFS:** build an adjacency list and count how many traversals are started from unvisited nodes — Time `O(n + E)`, Space `O(n + E)`.

## Key Takeaway

Counting components = `n` minus the number of successful unions; Union-Find handles this (and dynamic edge additions) elegantly.

## C++

```cpp
/*
    Graph of n nodes, given edges array, return # of connected components
    Ex. n = 5, edges = [[0,1],[1,2],[3,4]] -> 2

    Union find, for each edge combine, if already in same set keep traversing
    If not in same set, decrement count by 1, count will store # of components

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    int countComponents(int n, vector<vector<int>>& edges) {
        vector<int> parents;
        vector<int> ranks;
        for (int i = 0; i < n; i++) {
            parents.push_back(i);
            ranks.push_back(1);
        }
        
        int result = n;
        for (int i = 0; i < edges.size(); i++) {
            int n1 = edges[i][0];
            int n2 = edges[i][1];
            result -= doUnion(parents, ranks, n1, n2);
        }
        return result;
    }
private:
    int doFind(vector<int>& parents, int n) {
        int p = parents[n];
        while (p != parents[p]) {
            parents[p] = parents[parents[p]];
            p = parents[p];
        }
        return p;
    }
    
    int doUnion(vector<int>& parents, vector<int>& ranks, int n1, int n2) {
        int p1 = doFind(parents, n1);
        int p2 = doFind(parents, n2);
        if (p1 == p2) {
            return 0;
        }
        
        if (ranks[p1] > ranks[p2]) {
            parents[p2] = p1;
            ranks[p1] += ranks[p2];
        } else {
            parents[p1] = p2;
            ranks[p2] += ranks[p1];
        }
        
        return 1;
    }
};
```
