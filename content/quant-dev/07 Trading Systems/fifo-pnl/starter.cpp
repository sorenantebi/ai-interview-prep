#include <cstdint>
#include <optional>

enum class Side { Buy, Sell };

class PositionTracker {
public:
    void on_fill(Side side, std::int64_t price, std::int64_t qty) {}

    std::int64_t position() const { return 0; }
    std::int64_t realized_pnl() const { return 0; }
    std::int64_t unrealized_pnl(std::int64_t mark) const { return 0; }
    std::optional<double> average_cost() const { return std::nullopt; }
};
