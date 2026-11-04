---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/evaluate-division/
neetcode: https://neetcode.io/problems/evaluate-division
---
# Evaluate Division - Solution

## Intuition

Treat each variable as a node. An equation `A / B = k` gives a directed edge `A -> B` with weight `k` and a reverse edge `B -> A` with weight `1/k`. A query `C / D` is then the product of edge weights along any path from `C` to `D`. Since the input has no contradictions, any path gives the same product.

## Approach

1. Build an adjacency map: for each equation add `A -> B` with weight `k` and `B -> A` with weight `1/k`.
2. For each query `(C, D)`, if either variable is not in the graph, the answer is `-1.0`.
3. If `C == D` (and defined), the answer is `1.0`.
4. Otherwise run a DFS from `C`, multiplying weights along the path, until `D` is reached. Track visited nodes to avoid cycles.
5. If `D` is unreachable, the answer is `-1.0`.

## Code

```python
from typing import List, Optional
from collections import defaultdict

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        graph = defaultdict(dict)
        for (a, b), k in zip(equations, values):
            graph[a][b] = k
            graph[b][a] = 1.0 / k

        def dfs(src: str, dst: str, visited: set) -> float:
            if src == dst:
                return 1.0
            visited.add(src)
            for nxt, w in graph[src].items():
                if nxt in visited:
                    continue
                res = dfs(nxt, dst, visited)
                if res != -1.0:
                    return w * res
            return -1.0

        ans = []
        for c, d in queries:
            if c not in graph or d not in graph:
                ans.append(-1.0)
            else:
                ans.append(dfs(c, d, set()))
        return ans
```

## Complexity

- **Time:** `O(Q * (V + E))` — each query runs one DFS over the graph, where `V` and `E` are bounded by the number of equations.
- **Space:** `O(V + E)` — adjacency map plus recursion stack and visited set.

## Other Approaches

- **BFS per query:** same traversal done iteratively with a queue — Time `O(Q * (V + E))` / Space `O(V + E)`
- **Weighted Union-Find:** store each node's ratio to its root with path compression, so each query is near constant time — Time `O((E + Q) * α(V))` / Space `O(V)`
- **Floyd-Warshall:** precompute all-pairs ratios — Time `O(V^3 + Q)` / Space `O(V^2)`

## C++

```cpp
class Solution {
    unordered_map<string, vector<pair<string, double>>> graph;
    unordered_map<string, bool> visited;
    double queryAns;

public:
    bool dfs(string startNode, string endNode, double runningProduct){
        if(graph.find(startNode) == graph.end() || graph.find(endNode) == graph.end()) {
            return false;
        }
        
        if(startNode == endNode && graph.find(startNode)!=graph.end()) {
            queryAns = runningProduct;
            return true;
            
        }
        
        bool tempAns = false;
        visited[startNode] = true;
        
        for(int i = 0; i < graph[startNode].size(); i++){
            if(!visited[graph[startNode][i].first]){
                tempAns = dfs(graph[startNode][i].first, endNode, runningProduct*graph[startNode][i].second);
                if(tempAns){
                    break;
                }
            }
        }
        visited[startNode] = false;
        
        return tempAns;
    }
    
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        int n = equations.size(), m = queries.size();
        vector<double> ans(m);
        
        for(int i = 0; i < n ; i++){
            
            graph[equations[i][0]].push_back({equations[i][1], values[i]});
            graph[equations[i][1]].push_back({equations[i][0], 1/values[i]});
            visited[equations[i][0]] = false;
            visited[equations[i][1]] = false;

        }
        
        for(int i = 0; i < m ; i++){
            
            queryAns = 1;
            bool pathFound = dfs(queries[i][0], queries[i][1], 1);            
            if(pathFound) ans[i] = queryAns;
            else ans[i] = -1;
            
        }
        return ans;
    }
};
```
