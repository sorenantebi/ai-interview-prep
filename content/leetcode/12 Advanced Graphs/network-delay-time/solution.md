---
topic: "Advanced Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/network-delay-time/
neetcode: https://neetcode.io/problems/network-delay-time
---
# Network Delay Time - Solution

**Question:** Network Delay Time - Question · **Difficulty:** Medium

## Intuition

The time for the last node to hear the signal is the largest shortest-path distance from `k`. With non-negative edge weights, Dijkstra's algorithm computes all single-source shortest paths. If some node is never reached, the answer is `-1`.

## Approach

1. Build an adjacency list `u -> [(v, w)]`.
2. Run Dijkstra from `k` with a min-heap of `(time, node)`; record a node's distance the first time it is popped.
3. Skip nodes already finalised; otherwise push all neighbours with `time + w`.
4. If fewer than `n` nodes were finalised return `-1`, otherwise return the maximum distance.

## Code

```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        edges = collections.defaultdict(list)
        for u, v, w in times:
            edges[u].append((v, w))

        minHeap = [(0, k)]
        visit = set()
        t = 0
        while minHeap:
            w1, n1 = heapq.heappop(minHeap)
            if n1 in visit:
                continue
            visit.add(n1)
            t = w1

            for n2, w2 in edges[n1]:
                if n2 not in visit:
                    heapq.heappush(minHeap, (w1 + w2, n2))
        return t if len(visit) == n else -1

        # O(E * logV)
```

## Complexity

- **Time:** `O(E log E)` — each edge can push one heap entry.
- **Space:** `O(V + E)` — adjacency list, heap and distance map.

## Other Approaches

- **Bellman-Ford:** relax all edges `n - 1` times — Time `O(V·E)`, Space `O(V)`.
- **Floyd-Warshall:** all-pairs shortest paths, then read row `k` — Time `O(V^3)`, Space `O(V^2)`.

## Key Takeaway

"How long until everything is reached" from one source = max of single-source shortest paths; use Dijkstra with a "finalise on first pop" visited set when weights are non-negative.

## C++

```cpp
/*
    Signal sent from node k to network of n nodes, return time for all nodes to receive it
    Ex. times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2 -> 2
                  u,v,w -> u = source node, v = target node, w = signal travel time

    Shortest path from node k to every other node, Dijkstra's to find fastest path

    Time: O(V + E log V)
    Space: O(V + E)
*/

class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<pair<int, int>> adj[n + 1];
        for (int i = 0; i < times.size(); i++) {
            int source = times[i][0];
            int dest = times[i][1];
            int time = times[i][2];
            adj[source].push_back({time, dest});
        }
        
        vector<int> signalReceiveTime(n + 1, INT_MAX);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, k});
        
        // time for start node is 0
        signalReceiveTime[k] = 0;
        
        while (!pq.empty()) {
            int currNodeTime = pq.top().first;
            int currNode = pq.top().second;
            pq.pop();
            
            if (currNodeTime > signalReceiveTime[currNode]) {
                continue;
            }
            
            // send signal to adjacent nodes
            for (int i = 0; i < adj[currNode].size(); i++) {
                pair<int, int> edge = adj[currNode][i];
                int time = edge.first;
                int neighborNode = edge.second;
                
                // fastest signal time for neighborNode so far
                if (signalReceiveTime[neighborNode] > currNodeTime + time) {
                    signalReceiveTime[neighborNode] = currNodeTime + time;
                    pq.push({signalReceiveTime[neighborNode], neighborNode});
                }
            }
        }
        
        int result = INT_MIN;
        for (int i = 1; i <= n; i++) {
            result = max(result, signalReceiveTime[i]);
        }
        
        if (result == INT_MAX) {
            return -1;
        }
        return result;
    }
};
```
