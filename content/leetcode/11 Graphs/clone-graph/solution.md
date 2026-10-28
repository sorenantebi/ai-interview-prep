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

## C++

```cpp
/*
    Given ref of a node in connected undirected graph, return deep copy

    Both BFS & DFS work, map original node to its copy

    Time: O(m + n)
    Space: O(n)
*/

/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> neighbors;
    Node() {
        val = 0;
        neighbors = vector<Node*>();
    }
    Node(int _val) {
        val = _val;
        neighbors = vector<Node*>();
    }
    Node(int _val, vector<Node*> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
};
*/

// class Solution {
// public:
//     Node* cloneGraph(Node* node) {
//         if (node == NULL) {
//             return NULL;
//         } 
//         if (m.find(node) == m.end()) {
//             m[node] = new Node(node->val);
//             for (int i = 0; i < node->neighbors.size(); i++) {
//                 Node* neighbor = node->neighbors[i];
//                 m[node]->neighbors.push_back(cloneGraph(neighbor));
//             }
//         }
//         return m[node];
//     }
// private:
//     unordered_map<Node*, Node*> m;
// };

class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (node == NULL) {
            return NULL;
        }
        
        Node* copy = new Node(node->val);
        m[node] = copy;
        
        queue<Node*> q;
        q.push(node);
        
        while (!q.empty()) {
            Node* curr = q.front();
            q.pop();
            
            for (int i = 0; i < curr->neighbors.size(); i++) {
                Node* neighbor = curr->neighbors[i];
                
                if (m.find(neighbor) == m.end()) {
                    m[neighbor] = new Node(neighbor->val);
                    q.push(neighbor);
                }
                
                m[curr]->neighbors.push_back(m[neighbor]);
            }
        }
        
        return copy;
    }
private:
    unordered_map<Node*, Node*> m;
};
```
