#include <cstddef>
#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

enum class Side { Buy, Sell };
using OrderId = std::uint64_t;
using Price = std::int64_t;
using Qty = std::int64_t;

class OrderBook {
public:
    bool add(OrderId id, Side side, Price price, Qty qty) { return false; }

    bool cancel(OrderId id) { return false; }

    bool modify(OrderId id, Qty new_qty) { return false; }

    std::optional<std::pair<Price, Qty>> best_bid() const { return std::nullopt; }
    std::optional<std::pair<Price, Qty>> best_ask() const { return std::nullopt; }

    std::vector<std::pair<Price, Qty>> depth(Side side, std::size_t n) const { return {}; }

    Qty volume_at(Side side, Price price) const { return 0; }

    std::vector<OrderId> queue_at(Side side, Price price) const { return {}; }

    std::size_t order_count() const { return 0; }
};
