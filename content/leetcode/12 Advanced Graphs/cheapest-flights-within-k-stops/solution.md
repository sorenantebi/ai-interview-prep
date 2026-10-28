---
topic: "Advanced Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/cheapest-flights-within-k-stops/
neetcode: https://neetcode.io/problems/cheapest-flight-path
---
# Cheapest Flights Within K Stops - Solution

**Question:** Cheapest Flights Within K Stops - Question · **Difficulty:** Medium

## Intuition

The stop limit breaks plain Dijkstra (a cheaper path with more hops may block a slightly pricier one with fewer hops). **Bellman-Ford limited to `k + 1` rounds** fits exactly: after round `i`, `prices[v]` is the cheapest cost using at most `i` flights. Relaxing from a snapshot of the previous round prevents chaining several flights within one round.

## Approach

1. `prices = [inf] * n`, `prices[src] = 0`.
2. Repeat `k + 1` times: copy `prices` to `tmp`; for every flight `(u, v, w)` with finite `prices[u]`, set `tmp[v] = min(tmp[v], prices[u] + w)`; then `prices = tmp`.
3. Return `prices[dst]` or `-1` if it's still infinite.

## Code

```python
class Solution:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        prices = [float("inf")] * n
        prices[src] = 0

        for i in range(k + 1):
            tmpPrices = prices.copy()

            for s, d, p in flights:  # s=source, d=dest, p=price
                if prices[s] == float("inf"):
                    continue
                if prices[s] + p < tmpPrices[d]:
                    tmpPrices[d] = prices[s] + p
            prices = tmpPrices
        return -1 if prices[dst] == float("inf") else prices[dst]
```

## Complexity

- **Time:** `O(k · E)` — `k + 1` rounds over all flights.
- **Space:** `O(n)` — two price arrays.

## Other Approaches

- **BFS by levels with pruning:** expand level by level (one flight per level) up to `k + 1` levels, keeping best cost per city — Time `O(k · E)`, Space `O(n + E)`.
- **Dijkstra on state `(city, stops)`:** heap ordered by cost, track best stops per city to prune — Time `O(E · k · log(E · k))`, Space `O(n · k)`.

## Key Takeaway

When a shortest path has a hop limit, use Bellman-Ford with exactly `limit` rounds and a copy of the previous round's distances.

## C++

```cpp
/**
  This function uses the Bellman-Ford algorithm to find the cheapest price from source (src) to destination (dst)
  with at most k stops allowed. It iteratively relaxes the edges for k+1 iterations, updating the minimum
  cost to reach each vertex. The final result is the minimum cost to reach the destination, or -1 if the
  destination is not reachable within the given constraints.
  
  Space Complexity: O(n) - space used for the prices array.
  Time Complexity: O(k * |flights|) - k iterations, processing all flights in each iteration.
 */
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<int> prices(n, INT_MAX);
        prices[src] = 0;

        // Perform k+1 iterations of Bellman-Ford algorithm.
        for (int i = 0; i < k + 1; i++) {
            vector<int> tmpPrices(begin(prices), end(prices));

            for (auto it : flights) {
                int s = it[0];
                int d = it[1];
                int p = it[2];

                if (prices[s] == INT_MAX) continue;

                if (prices[s] + p < tmpPrices[d]) {
                    tmpPrices[d] = prices[s] + p;
                }
            }
            prices = tmpPrices;
        }
        return prices[dst] == INT_MAX ? -1 : prices[dst];
    }
};


/*
    Given cities connected by flights [from,to,price], also given src, dst, & k:
    Return cheapest price from src to dst with at most k stops

    Dijkstra's but modified, normal won't work b/c will discard heap nodes w/o finishing
    Modify: need to re-consider a node if dist from source is shorter than what we recorded
    But, if we encounter node already processed but # of stops from source is lesser,
    Need to add it back to the heap to be considered again

    Time: O(V^2 log V) -> V = number of cities
    Space: O(V^2)
*/

class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        // build adjacency matrix
        vector<vector<int>> adj(n, vector<int>(n));
        for (int i = 0; i < flights.size(); i++) {
            vector<int> flight = flights[i];
            adj[flight[0]][flight[1]] = flight[2];
        }
        
        // shortest distances
        vector<int> distances(n, INT_MAX);
        distances[src] = 0;
        // shortest steps
        vector<int> currStops(n, INT_MAX);
        currStops[src] = 0;
        
        // priority queue -> (cost, node, stops)
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq;
        pq.push({0, src, 0});
        
        while (!pq.empty()) {
            int cost = pq.top()[0];
            int node = pq.top()[1];
            int stops = pq.top()[2];
            pq.pop();
            
            // if destination is reached, return cost to get here
            if (node == dst) {
                return cost;
            }
            
            // if no more steps left, continue
            if (stops == k + 1) {
                continue;
            }
            
            // check & relax all neighboring edges
            for (int neighbor = 0; neighbor < n; neighbor++) {
                if (adj[node][neighbor] > 0) {
                    int currCost = cost;
                    int neighborDist = distances[neighbor];
                    int neighborWeight = adj[node][neighbor];
                    
                    // check if better cost
                    int currDist = currCost + neighborWeight;
                    if (currDist < neighborDist || stops + 1 < currStops[neighbor]) {
                        pq.push({currDist, neighbor, stops + 1});
                        distances[neighbor] = currDist;
                        currStops[neighbor] = stops;
                    } else if (stops < currStops[neighbor]) {
                        // check if better steps
                        pq.push({currDist, neighbor, stops + 1});
                    }
                    currStops[neighbor] = stops;
                }
            }
        }
        
        if (distances[dst] == INT_MAX) {
            return -1;
        }
        return distances[dst];
    }
};
```
