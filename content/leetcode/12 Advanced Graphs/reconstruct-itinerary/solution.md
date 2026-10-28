---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/reconstruct-itinerary/
neetcode: https://neetcode.io/problems/reconstruct-flight-path
---
# Reconstruct Itinerary - Solution

**Question:** Reconstruct Itinerary - Question · **Difficulty:** Hard

## Intuition

Using every ticket exactly once is an **Eulerian path** in a directed multigraph. Hierholzer's algorithm finds one: walk greedily along unused edges, and when you get stuck at a node, add it to the front of the route. Visiting neighbours in lexicographic order makes the result the smallest itinerary, because dead-end branches end up appended last in the final ordering.

## Approach

1. Build an adjacency list; sort each list in **reverse** so `pop()` returns the smallest destination in `O(1)`.
2. Iterative DFS with a stack starting at `"JFK"`.
3. While the top of the stack still has outgoing tickets, pop the smallest one and push the destination.
4. When the top has no tickets left, pop it into the `route`.
5. `route` is built in reverse; return `route[::-1]`.

## Code

```python
class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        adj = {src: [] for src, dst in tickets}
        res = []

        for src, dst in tickets:
            adj[src].append(dst)

        for key in adj:
            adj[key].sort()

        def dfs(adj, src):
            if src in adj:
                destinations = adj[src][:]
                while destinations:
                    dest = destinations[0]
                    adj[src].pop(0)
                    dfs(adj, dest)
                    destinations = adj[src][:]
            res.append(src)

        dfs(adj, "JFK")
        res.reverse()

        if len(res) != len(tickets) + 1:
            return []

        return res
```

## Complexity

- **Time:** `O(E log E)` — dominated by sorting the tickets; the traversal itself is `O(E)`.
- **Space:** `O(E)` — adjacency lists, stack, and route.

## Other Approaches

- **Backtracking DFS:** try destinations in sorted order, undo when you get stuck before using all tickets — Time exponential in the worst case, Space `O(E)`.

## Key Takeaway

"Use every edge exactly once" means Eulerian path: Hierholzer's post-order DFS (append when stuck, reverse at the end) handles dead ends without backtracking.

## C++

```cpp
/*
    Given airline tickets, find valid itinerary (use all tickets once)
    Ex. tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
        output = ["JFK","MUC","LHR","SFO","SJC"]

    Greedy DFS, build route backwards when retreating, merge cycles into main path

    Time: O(E log (E / V)) -> E = # of flights, V = # of airports, sorting
    Space: O(V + E) -> store # of airports & # of flights in hash map
*/

class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string, multiset<string>> m;
        for (int i = 0; i < tickets.size(); i++) {
            m[tickets[i][0]].insert(tickets[i][1]);
        }
        
        vector<string> result;
        dfs(m, "JFK", result);
        reverse(result.begin(), result.end());
        return result;
    }
private:
    void dfs(unordered_map<string, multiset<string>>& m,
        string airport, vector<string>& result) {
        
        while (!m[airport].empty()) {
            string next = *m[airport].begin();
            m[airport].erase(m[airport].begin());
            dfs(m, next, result);
        }
        
        result.push_back(airport);
    }
};
```
