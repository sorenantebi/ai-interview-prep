---
topic: "Trading Systems"
difficulty: Medium
---
# FIFO Position & P&L Tracker - Solution

## Intuition

All open lots always have the same sign as the position (you can't be long and short at once), so they fit in one FIFO queue. A fill in the same direction as the position appends a lot; a fill in the opposite direction eats lots from the front, realizing P&L on each, and if it is bigger than the whole position the leftover becomes a new lot on the other side.

For O(1) queries, keep two running numbers next to the queue: the signed position and the **open cost** `sum(lot.price * lot.qty)`. Then:

- `average_cost = open_cost / |position|`
- `unrealized = sign(position) * (mark * |position| - open_cost)`

## Approach

1. Let `dir = +1` for a buy and `-1` for a sell.
2. While `qty > 0` and the position has the opposite sign of `dir`: take the front lot, close `q = min(qty, lot.qty)`. Realized P&L of closing a long with a sell is `(price - lot.price) * q`, of closing a short with a buy `(lot.price - price) * q`; both equal `-dir * (price - lot.price) * q`. Update position, open cost, and pop the lot when it reaches 0.
3. If `qty` is still positive, push a new lot `(price, qty)` and update position and open cost.

## Code

```cpp
#include <algorithm>
#include <cstdint>
#include <deque>
#include <optional>

enum class Side { Buy, Sell };

class PositionTracker {
public:
    void on_fill(Side side, std::int64_t price, std::int64_t qty) {
        const std::int64_t dir = side == Side::Buy ? 1 : -1;
        while (qty > 0 && position_ * dir < 0) {  // fill reduces the position
            Lot& lot = lots_.front();
            const std::int64_t q = std::min(qty, lot.qty);
            realized_ += -dir * (price - lot.price) * q;
            open_cost_ -= lot.price * q;
            position_ += dir * q;
            lot.qty -= q;
            qty -= q;
            if (lot.qty == 0) lots_.pop_front();
        }
        if (qty > 0) {  // what is left opens (or extends) a position in the fill's direction
            lots_.push_back({price, qty});
            open_cost_ += price * qty;
            position_ += dir * qty;
        }
    }

    std::int64_t position() const { return position_; }
    std::int64_t realized_pnl() const { return realized_; }

    std::int64_t unrealized_pnl(std::int64_t mark) const {
        const std::int64_t abs_pos = position_ < 0 ? -position_ : position_;
        const std::int64_t long_pnl = mark * abs_pos - open_cost_;
        return position_ < 0 ? -long_pnl : long_pnl;
    }

    std::optional<double> average_cost() const {
        if (position_ == 0) return std::nullopt;
        const std::int64_t abs_pos = position_ < 0 ? -position_ : position_;
        return static_cast<double>(open_cost_) / static_cast<double>(abs_pos);
    }

private:
    struct Lot { std::int64_t price, qty; };
    std::deque<Lot> lots_;
    std::int64_t position_ = 0, realized_ = 0, open_cost_ = 0;
};
```

## Complexity

- Time: `on_fill` O(1) amortized (each lot is pushed once and popped once; a fill touches at most one lot it doesn't pop); every query O(1).
- Space: O(open lots).

## Interview follow-ups

- **Other accounting methods.** Average-cost (one blended lot: realize against the average price) needs no queue at all; LIFO uses a stack. Trading desks often use average cost for risk, while tax and regulatory reports may require FIFO. They give the same total P&L once flat, but different realized/unrealized splits along the way.
- **Fees and rebates.** Exchange fees, maker rebates and financing costs go into realized P&L per fill.
- **Overflow and units.** Prices in ticks times quantities can overflow `int64` for big notionals or tiny tick sizes; use `__int128` or track P&L per tick-value currency. Convert to money (`ticks * tick_value * multiplier`) only for display.
- **Multi-threading.** Fills come from the order gateway, marks from market data: keep the tracker single-writer (one thread owns it) and publish snapshots for risk checks rather than locking on every fill.
- **Real-time risk.** Position limits and max-loss kill switches check these numbers before each new order, so `position()` and `unrealized_pnl()` must be O(1).
