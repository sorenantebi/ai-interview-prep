#include <cstddef>
#include <cstdint>

class Throttler {
public:
    Throttler(std::size_t max_msgs, std::uint64_t window_ns) {}

    bool allow(std::uint64_t client_id, std::uint64_t ts_ns) { return true; }
};
