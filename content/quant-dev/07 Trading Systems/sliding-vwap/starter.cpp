#include <cstdint>
#include <optional>

class SlidingVwap {
public:
    explicit SlidingVwap(std::uint64_t window_ns) {}

    void on_trade(std::uint64_t ts_ns, std::int64_t price, std::int64_t qty) {}

    std::optional<double> vwap(std::uint64_t now_ns) { return std::nullopt; }
};
