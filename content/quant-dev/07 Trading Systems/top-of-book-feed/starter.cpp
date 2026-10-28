#include <cstdint>
#include <optional>
#include <stdexcept>
#include <utility>

enum class Side { Bid, Ask };

struct Quote {
    std::optional<std::pair<std::int64_t, std::int64_t>> bid;
    std::optional<std::pair<std::int64_t, std::int64_t>> ask;
    std::optional<std::int64_t> spread;
    bool crossed = false;
    bool operator==(const Quote&) const = default;
};

class TopOfBook {
public:
    Quote apply(Side side, std::int64_t price, std::int64_t new_qty) { return {}; }

    Quote quote() const { return {}; }

    std::optional<double> mid() const { return std::nullopt; }
};
