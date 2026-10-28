#include <cstddef>
#include <cstdint>
#include <vector>

template <class V>
class HashMap {
public:
    HashMap() {}
    bool insert(std::int64_t key, const V& value) { return false; }
    V* find(std::int64_t key) { return nullptr; }
    const V* find(std::int64_t key) const { return nullptr; }
    bool erase(std::int64_t key) { return false; }
    std::size_t size() const noexcept { return 0; }
    std::size_t capacity() const noexcept { return 0; }
};
