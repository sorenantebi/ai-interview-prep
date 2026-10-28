---
topic: "Containers & Allocators"
difficulty: Medium
---
# LRU Cache - Solution

## Intuition

Two needs, two structures:

- O(1) lookup by key: a hash map.
- O(1) "move this entry to the front" and "drop the entry at the back": a doubly linked list ordered by recency.

Link them by storing, for each key, the list *iterator* of its node. `std::list::splice` moves a node to the front without invalidating any iterator, so the map entries stay valid forever. The least recently used entry is always `list.back()`, and its key is stored in the node, so the map entry can be erased too.

## Approach

1. `std::list<std::pair<K, V>> order_` (front = most recent) and `std::unordered_map<K, list::iterator> index_`.
2. `get(key)`: look up; if missing return `nullopt`; otherwise `splice` the node to the front and return its value.
3. `put(key, value)`:
   - if present: overwrite the value and splice to the front;
   - otherwise push a new node to the front and add it to the map; if the size now exceeds the capacity, erase `order_.back()` from the map and pop it.
4. `contains`: a map lookup only, so the order is untouched.

## Code

```cpp
#include <cstddef>
#include <list>
#include <optional>
#include <unordered_map>
#include <utility>

template <class K, class V>
class LRUCache {
public:
    explicit LRUCache(std::size_t capacity) : cap_(capacity) { index_.reserve(capacity); }

    std::optional<V> get(const K& key) {
        auto it = index_.find(key);
        if (it == index_.end()) return std::nullopt;
        order_.splice(order_.begin(), order_, it->second);
        return it->second->second;
    }

    void put(const K& key, const V& value) {
        if (auto it = index_.find(key); it != index_.end()) {
            it->second->second = value;
            order_.splice(order_.begin(), order_, it->second);
            return;
        }
        order_.emplace_front(key, value);
        index_.emplace(key, order_.begin());
        if (order_.size() > cap_) {
            index_.erase(order_.back().first);
            order_.pop_back();
        }
    }

    bool contains(const K& key) const { return index_.count(key) != 0; }
    std::size_t size() const noexcept { return order_.size(); }

private:
    std::size_t cap_;
    std::list<std::pair<K, V>> order_;  // front = most recently used
    std::unordered_map<K, typename std::list<std::pair<K, V>>::iterator> index_;
};
```

## Complexity

- Time: O(1) average for `get`, `put`, `contains` (hash lookup + constant pointer updates).
- Space: O(capacity): one list node and one map entry per key.

## Interview follow-ups

- `std::list` allocates a node per insert. Rewrite it with a preallocated array of nodes and integer `prev`/`next` indices (an intrusive list) so steady-state `put` never allocates.
- Make it thread-safe. Why does even `get` need exclusive access in an LRU (it mutates the order)? How do sharding or "approximate LRU" (CLOCK) reduce contention?
- Add a time-to-live per entry, so stale prices expire even if they were used recently.
- LFU instead of LRU: evict the least *frequently* used key in O(1).
