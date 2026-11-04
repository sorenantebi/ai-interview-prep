---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/design-hashmap/
neetcode: https://neetcode.io/problems/design-hashmap
---
# Design HashMap - Solution

## Intuition

A hash map maps keys to buckets with a hash function and resolves collisions inside each bucket. Using a fixed number of buckets and a simple modulo hash keeps things simple. Each bucket holds a small list of `[key, value]` pairs (separate chaining), so colliding keys coexist.

## Approach

1. Allocate a fixed number of buckets (a prime, `1009`) to spread keys evenly.
2. Hash a key with `key % size` to pick its bucket.
3. `put`: scan the bucket; if the key is found, update its value, otherwise append a new pair.
4. `get`: scan the bucket; return the value if the key is found, otherwise `-1`.
5. `remove`: scan the bucket and delete the pair if the key is found.

## Code

```python
class ListNode:
    def __init__(self, key=-1, val=-1, next=None):
        self.key = key
        self.val = val
        self.next = next

class MyHashMap:
    def __init__(self):
        self.map = [ListNode() for i in range(1000)]
        
    def hashcode(self, key):
        return key % len(self.map)

    def put(self, key: int, value: int) -> None:
        cur = self.map[self.hashcode(key)]
        while cur.next:
            if cur.next.key == key:
                cur.next.val = value
                return
            cur = cur.next
        cur.next = ListNode(key, value)
         
    def get(self, key: int) -> int:
        cur = self.map[self.hashcode(key)].next
        while cur and cur.key != key:
            cur = cur.next
        if cur:
            return cur.val
        return -1

    def remove(self, key: int) -> None:
        cur = self.map[self.hashcode(key)]
        while cur.next and cur.next.key != key:
            cur = cur.next
        if cur and cur.next:
            cur.next = cur.next.next
```

## Complexity

- **Time:** `O(n / b)` per operation on average — a bucket holds about `n / b` pairs for `n` keys and `b` buckets, so with a fixed `b` and at most `10^4` operations this is effectively constant.
- **Space:** `O(b + n)` — the bucket array plus one pair per stored key.

## Other Approaches

- **Direct-address array:** allocate an array of size `10^6 + 1` initialized to `-1` and index it by key — Time `O(1)` / Space `O(10^6)`
- **Linked-list buckets:** chain nodes in each bucket instead of Python lists, giving cheap removal once the node is found — Time `O(n / b)` / Space `O(b + n)`
- **Dynamic resizing:** grow the bucket array when the load factor gets too high to keep chains short — Time `O(1)` amortized / Space `O(b + n)`

## C++

```cpp
/*
    Design a HashMap without using any built-in hash table libraries.

    Designing a hash table using the chaining method, where a vector holds a list of pairs representing the key-value mappings.

    Time: O(n)
    Space: O(n)
*/

class MyHashMap {
public:
    const int N = 10010;
    vector<list<pair<int, int>>> h; 

    /** Initialize your data structure here. */
    MyHashMap() {
        h = vector<list<pair<int, int>>>(N);
    }
    
    list<pair<int, int>>::iterator find(int key) {
        int t = key % N;
        for (auto it = h[t].begin(); it != h[t].end(); it ++ ) {
            if (it->first == key)
                return it;
        }
        return h[t].end();
    }

    /** value will always be non-negative. */
    void put(int key, int value) {
        auto t = key % N;
        auto it = find(key);
        if (it == h[t].end()) h[t].push_back({key, value});
        else it->second = value;
    }
    
    /** Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key */
    int get(int key) {
        auto t = key % N;
        auto it = find(key);
        if (it != h[t].end()) return it->second;
        return -1;
    }
    
    /** Removes the mapping of the specified value key if this map contains a mapping for the key */
    void remove(int key) {
        auto t = key % N;
        auto it = find(key);
        if (it != h[t].end()) h[t].erase(it);
    }
};

/**
 * Your MyHashMap object will be instantiated and called as such:
 * MyHashMap* obj = new MyHashMap();
 * obj->put(key,value);
 * int param_2 = obj->get(key);
 * obj->remove(key);
 */
```
