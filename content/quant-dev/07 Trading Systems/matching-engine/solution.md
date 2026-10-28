---
topic: "Trading Systems"
difficulty: Hard
---
# Price-Time Priority Matching Engine - Solution

## Intuition

Matching is a loop over the opposite side of the book, best level first, front of the queue first: trade `min(remaining, maker qty)`, shrink both, drop the maker when it hits zero, drop the level when it empties, and stop when the taker is done or the best opposite price no longer crosses. A limit order and a market order run the same loop; they differ only in the "does it still cross?" test and in what happens to the leftover.

The book itself is the same structure as a resting limit order book: sorted price levels (best at `begin()`), a FIFO list per level, and an id index for O(1) cancel.

## Approach

1. Bids in `std::map<Price, Level, std::greater<>>`, asks in `std::map<Price, Level>`; each `Level` holds a running total and a `std::list` of `(id, qty)`.
2. `index_` maps a resting id to its side, price and list iterator.
3. `match(book, taker, qty, crosses)`: while `qty > 0`, the book is not empty and `crosses(best price)`, trade with the front of the best level as described above. Fills are emitted at the level's (maker's) price.
4. `submit_limit`: buys match against asks with `crosses = ask <= price`, sells against bids with `bid >= price`; then rest any remainder at the back of its own level.
5. `submit_market`: same with `crosses` always true; the remainder is discarded.
6. `cancel`: unlink via the stored iterator, fix the level total, erase an empty level.

## Code

```cpp
#include <algorithm>
#include <cstdint>
#include <functional>
#include <iterator>
#include <list>
#include <map>
#include <optional>
#include <unordered_map>
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
    std::vector<Fill> submit_limit(OrderId id, Side side, Price price, Qty qty) {
        std::vector<Fill> fills;
        if (qty <= 0) return fills;
        if (side == Side::Buy) {
            match(asks_, id, qty, [&](Price ask) { return ask <= price; }, fills);
            if (qty > 0) rest(bids_, id, side, price, qty);
        } else {
            match(bids_, id, qty, [&](Price bid) { return bid >= price; }, fills);
            if (qty > 0) rest(asks_, id, side, price, qty);
        }
        return fills;
    }

    std::vector<Fill> submit_market(OrderId id, Side side, Qty qty) {
        std::vector<Fill> fills;
        auto any = [](Price) { return true; };
        if (side == Side::Buy) match(asks_, id, qty, any, fills);
        else match(bids_, id, qty, any, fills);
        return fills;  // leftover qty is simply dropped
    }

    bool cancel(OrderId id) {
        auto it = index_.find(id);
        if (it == index_.end()) return false;
        const Loc loc = it->second;
        if (loc.side == Side::Buy) unlink(bids_, loc);
        else unlink(asks_, loc);
        index_.erase(it);
        return true;
    }

    std::optional<std::pair<Price, Qty>> best_bid() const { return best(bids_); }
    std::optional<std::pair<Price, Qty>> best_ask() const { return best(asks_); }

    Qty resting_qty(OrderId id) const {
        auto it = index_.find(id);
        return it == index_.end() ? 0 : it->second.pos->qty;
    }

private:
    struct Resting { OrderId id; Qty qty; };
    struct Level { Qty total = 0; std::list<Resting> queue; };
    struct Loc { Side side; Price price; std::list<Resting>::iterator pos; };

    template <class Book, class Crosses>
    void match(Book& book, OrderId taker, Qty& qty, Crosses crosses, std::vector<Fill>& fills) {
        while (qty > 0 && !book.empty() && crosses(book.begin()->first)) {
            auto lvl = book.begin();
            Level& level = lvl->second;
            while (qty > 0 && !level.queue.empty()) {
                Resting& maker = level.queue.front();
                Qty traded = std::min(qty, maker.qty);
                fills.push_back({maker.id, taker, lvl->first, traded});
                qty -= traded;
                maker.qty -= traded;
                level.total -= traded;
                if (maker.qty == 0) {
                    index_.erase(maker.id);
                    level.queue.pop_front();
                }
            }
            if (level.queue.empty()) book.erase(lvl);
        }
    }

    template <class Book>
    void rest(Book& book, OrderId id, Side side, Price price, Qty qty) {
        Level& level = book[price];
        level.total += qty;
        level.queue.push_back({id, qty});
        index_.emplace(id, Loc{side, price, std::prev(level.queue.end())});
    }

    template <class Book>
    void unlink(Book& book, const Loc& loc) {
        auto lvl = book.find(loc.price);
        lvl->second.total -= loc.pos->qty;
        lvl->second.queue.erase(loc.pos);
        if (lvl->second.queue.empty()) book.erase(lvl);
    }

    template <class Book>
    static std::optional<std::pair<Price, Qty>> best(const Book& book) {
        if (book.empty()) return std::nullopt;
        return std::pair{book.begin()->first, book.begin()->second.total};
    }

    std::map<Price, Level, std::greater<Price>> bids_;
    std::map<Price, Level> asks_;
    std::unordered_map<OrderId, Loc> index_;
};
```

## Complexity

- Time: an order that touches `L` levels and produces `F` fills costs O(L log P + F); resting is O(log P); `cancel` O(1) expected for the lookup plus O(log P) to find the level; `best_*` O(1).
- Space: O(resting orders + levels).

## Interview follow-ups

- **Latency.** On the hot path, avoid `std::map`/`std::list` node allocations: preallocate order objects in a pool, use intrusive lists and an array-based price ladder around the current price. Return fills through a callback or a reusable buffer instead of a fresh `std::vector` per order.
- **Order types.** IOC (immediate-or-cancel: like the market logic but with a limit price), FOK (fill-or-kill: check available quantity first, all or nothing), post-only (reject or reprice if it would cross), stop orders, iceberg orders (only a slice is visible; the refill goes to the back of the queue).
- **Self-trade prevention.** Real venues stop a firm trading with itself: cancel the resting order, the incoming one, or both.
- **Other allocation rules.** Some futures markets use pro-rata matching (fill makers in proportion to their size) instead of FIFO, or a mix (top order priority, then pro-rata).
- **Determinism and recovery.** Exchanges run the engine single-threaded per instrument and sequence every input, so the whole book can be rebuilt by replaying the journal; primary/backup engines stay in lockstep that way.
- **Output.** Every fill produces two execution reports (maker and taker) and a public trade message; every book change produces a market-data update.
