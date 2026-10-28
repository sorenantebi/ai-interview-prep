#include <atomic>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <type_traits>

template <class T>
class SeqLock {
    static_assert(std::is_trivially_copyable_v<T>, "SeqLock needs a trivially copyable T");

public:
    explicit SeqLock(const T& initial = T{}) {}

    void write(const T& value) {}

    T read() const { return T{}; }

    std::uint64_t sequence() const { return 0; }
};
