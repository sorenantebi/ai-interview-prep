---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/clone-graph/
neetcode: https://neetcode.io/problems/clone-graph
---
# Clone Graph - Solution

**Question:** Clone Graph - Question · **Difficulty:** Medium

## Intuition

Traverse the original graph while maintaining a hash map `old node -> new node`. The map does double duty: it tells us which nodes have already been cloned (so cycles don't cause infinite loops) and lets us wire each clone's neighbors to the *cloned* neighbor objects.

## Approach

1. If `node` is `None`, return `None`.
2. Create the clone of the start node and put it in `clones`; push the original onto a BFS queue.
3. Pop a node `cur`. For each neighbor `nb`:
   - If `nb` has no clone yet, create it, store it in the map, and enqueue `nb`.
   - Append `clones[nb]` to `clones[cur].neighbors`.
4. When the queue is empty, return `clones[node]`.

## Code

```python
class Solution:
    def cloneGraph(self, node: "Node") -> "Node":
        oldToNew = {}

        def dfs(node):
            if node in oldToNew:
                return oldToNew[node]

            copy = Node(node.val)
            oldToNew[node] = copy
            for nei in node.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy

        return dfs(node) if node else None
```

## Complexity

- **Time:** `O(V + E)` — each node is cloned once and each edge (in both directions) is processed once.
- **Space:** `O(V)` — the hash map and BFS queue (excluding the output graph).

## Other Approaches

- **Recursive DFS with memo:** `clone(n)` returns `clones[n]` if present, otherwise creates it, stores it *before* recursing, then clones neighbors — Time `O(V + E)`, Space `O(V)` (recursion stack).

## Key Takeaway

Copying any structure with cycles or shared references (graphs, random-pointer lists) uses an `old -> new` map: register the copy before exploring its neighbors.
