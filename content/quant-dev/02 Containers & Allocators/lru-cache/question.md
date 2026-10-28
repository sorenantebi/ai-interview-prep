---
topic: "Containers & Allocators"
difficulty: Medium
---
# LRU Cache

**Topic:** Containers & Allocators · **Difficulty:** Medium

## Problem

A pricing service caches expensive results (implied volatilities, fair values for an instrument at a given spot) but can only keep a bounded number of them in memory. When the cache is full, the entry that has gone unused the longest is the best one to drop. Every lookup and every insert must stay O(1), because the cache sits on the request path.

Implement `LRUCache<K, V>`:

```cpp
template <class K, class V>
class LRUCache {
public:
    explicit LRUCache(std::size_t capacity);    // capacity >= 1
    std::optional<V> get(const K& key);         // value if present (and marks key most recently used), else nullopt
    void put(const K& key, const V& value);     // insert or update; marks key most recently used;
                                                // if this makes size() exceed capacity, evict the least recently used key
    bool contains(const K& key) const;          // presence check that does NOT change the recency order
    std::size_t size() const noexcept;
};
```

`K` is hashable with `std::hash<K>` and comparable with `==`.

## Examples

**Example 1**
```cpp
LRUCache<int, std::string> c(2);
c.put(1, "one");
c.put(2, "two");
c.get(1);          // "one"   (1 is now the most recent)
c.put(3, "three"); // evicts 2, the least recently used
c.get(2);          // std::nullopt
c.get(3);          // "three"
c.size();          // 2
```

**Example 2**
```cpp
LRUCache<std::string, double> vol(2);
vol.put("AAPL", 0.25);
vol.put("MSFT", 0.22);
vol.put("AAPL", 0.27);   // update counts as a use: MSFT is now the oldest
vol.put("NVDA", 0.55);   // evicts MSFT
vol.contains("MSFT");    // false
vol.get("AAPL");         // 0.27
```

## Constraints

- `get`, `put` and `contains` are O(1) on average.
- `1 <= capacity <= 10^6`; up to 10^6 operations.
