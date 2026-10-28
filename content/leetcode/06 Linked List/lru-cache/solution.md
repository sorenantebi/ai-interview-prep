---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/lru-cache/
neetcode: https://neetcode.io/problems/lru-cache
---
# LRU Cache - Solution

**Question:** LRU Cache - Question · **Difficulty:** Medium

## Intuition

We need `O(1)` lookup by key (hash map) **and** `O(1)` reordering by recency (doubly linked list). The map stores `key → node`; the list keeps nodes ordered from least to most recently used. Sentinel `left` (LRU end) and `right` (MRU end) nodes eliminate null checks when inserting or removing.

## Approach

1. Keep `cache: dict[key, Node]` and a doubly linked list `left <-> ... <-> right`.
2. Helper `remove(node)` unlinks a node; helper `insert(node)` places it just before `right` (most recent).
3. `get(key)`: if present, move its node to the MRU end and return its value; else `-1`.
4. `put(key, value)`: if present, unlink the old node. Create/insert the new node at the MRU end and store it in the map. If `len(cache) > capacity`, evict `left.next` (the LRU node) from both list and map.

## Code

```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # map key to node

        self.left, self.right = Node(0, 0), Node(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    # remove node from list
    def remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    # insert node at right
    def insert(self, node):
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.next, node.prev = nxt, prev

    def get(self, key: int) -> int:
        if key in self.cache:
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.remove(self.cache[key])
        self.cache[key] = Node(key, value)
        self.insert(self.cache[key])

        if len(self.cache) > self.cap:
            # remove from the list and delete the LRU from hashmap
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]
```

## Complexity

- **Time:** `O(1)` average per `get`/`put` — hash lookups plus constant pointer updates.
- **Space:** `O(capacity)` — one map entry and one list node per stored key.

## Other Approaches

- **`collections.OrderedDict`:** `move_to_end(key)` on access and `popitem(last=False)` to evict — Time `O(1)`, Space `O(capacity)`; concise, but interviewers usually want the manual version.
- **List/array of keys ordered by recency:** reordering is `O(capacity)` per op — Time `O(capacity)`, Space `O(capacity)`.

## Key Takeaway

Hash map + doubly linked list (with sentinels) is the standard recipe for `O(1)` ordered caches; store the key inside each node so eviction can delete it from the map.

## C++

```cpp
/*
    Design data structure that follows constraints of an LRU cache

    Hash map + doubly linked list, left = LRU, right = MRU
    get: update to MRU, put: update to MRU, remove LRU if full

    Time: O(1)
    Space: O(capacity)
*/

class Node {
public:
    int k;
    int val;
    Node* prev;
    Node* next;
    
    Node(int key, int value) {
        k = key;
        val = value;
        prev = NULL;
        next = NULL;
    }
};

class LRUCache {
public:
    LRUCache(int capacity) {
        cap = capacity;
        
        left = new Node(0, 0);
        right = new Node(0, 0);
        
        left->next = right;
        right->prev = left;
    }
    
    int get(int key) {
        if (cache.find(key) != cache.end()) {
            remove(cache[key]);
            insert(cache[key]);
            return cache[key]->val;
        }
        return -1;
    }
    
    void put(int key, int value) {
        if (cache.find(key) != cache.end()) {
            remove(cache[key]);
            
            // Free allocated memory for the removed node
            delete cache[key];
        }
        cache[key] = new Node(key, value);
        insert(cache[key]);
        
        if (cache.size() > cap) {
            // remove from list & delete LRU from map
            Node* lru = left->next;
            remove(lru);
            cache.erase(lru->k);
            
            // Free allocated memory for the removed node
            delete lru;
        }
    }
private:
    int cap;
    unordered_map<int, Node*> cache; // {key -> node}
    Node* left;
    Node* right;
    
    // remove node from list
    void remove(Node* node) {
        Node* prev = node->prev;
        Node* next = node->next;
        
        prev->next = next;
        next->prev = prev;
    }
    
    // insert node at right
    void insert(Node* node) {
        Node* prev = right->prev;
        Node* next = right;
        
        prev->next = node;
        next->prev = node;
        
        node->prev = prev;
        node->next = next;
    }
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
```
