#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

enum class Side { Buy, Sell };
using OrderId = std::uint64_t;
using Price = std::int64_t;
using Qty = std::int64_t;

struct Fill {
    OrderId maker_id;
    OrderId taker_id;
    Price price;
    Qty qty;
    bool operator==(const Fill&) const = default;
};

class MatchingEngine {
public:
    std::vector<Fill> submit_limit(OrderId id, Side side, Price price, Qty qty) { return {}; }

    std::vector<Fill> submit_market(OrderId id, Side side, Qty qty) { return {}; }

    bool cancel(OrderId id) { return false; }

    std::optional<std::pair<Price, Qty>> best_bid() const { return std::nullopt; }
    std::optional<std::pair<Price, Qty>> best_ask() const { return std::nullopt; }

    Qty resting_qty(OrderId id) const { return 0; }
};
