#include <cstddef>
#include <list>
#include <optional>
#include <unordered_map>
#include <utility>

template <class K, class V>
class LRUCache {
public:
    explicit LRUCache(std::size_t capacity) {}
    std::optional<V> get(const K& key) { return std::nullopt; }
    void put(const K& key, const V& value) {}
    bool contains(const K& key) const { return false; }
    std::size_t size() const noexcept { return 0; }
};
