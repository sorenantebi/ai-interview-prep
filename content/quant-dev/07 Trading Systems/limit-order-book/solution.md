---
topic: "Trading Systems"
difficulty: Hard
---
# Limit Order Book - Solution

## Intuition

Two questions must be fast: "what is the best price on each side?" and "where is order 12345?". A sorted map from price to level answers the first (the best level is `begin()`), and a hash map from order id to the order's exact position answers the second. Inside a level, a linked list keeps time priority and lets us unlink any order in O(1) once we hold its iterator.

Each level also caches its total quantity, so top-of-book and depth queries never walk the orders.

## Approach

1. Bids: `std::map<Price, Level, std::greater<Price>>` (highest first). Asks: `std::map<Price, Level>` (lowest first). So the best level of either side is `begin()`.
2. `Level` = running `total` + `std::list` of `(id, qty)` in arrival order.
3. `orders_`: `unordered_map<OrderId, Loc>` where `Loc` holds side, price and the list iterator. `std::list` iterators stay valid while other elements are inserted or erased, which is exactly what we need.
4. `add`: find-or-create the level, `push_back`, update `total`, record the iterator.
5. `cancel`: look up the iterator, subtract from `total`, erase from the list, erase the level if it became empty, erase the id.
6. `modify`: a reduction edits the quantity in place (keeps the queue spot); an increase is cancel + add (back of the queue).
7. The two maps have different types, so a small helper `on(side, f)` calls a generic lambda with the right one.

## Code

```cpp
#include <cstddef>
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

class OrderBook {
    // Defined first: functions with a deduced return type must be seen before use.
    struct Resting { OrderId id; Qty qty; };
    struct Level { Qty total = 0; std::list<Resting> queue; };
    struct Loc { Side side; Price price; std::list<Resting>::iterator pos; };

    template <class F> auto on(Side s, F&& f) { return s == Side::Buy ? f(bids_) : f(asks_); }
    template <class F> auto on(Side s, F&& f) const { return s == Side::Buy ? f(bids_) : f(asks_); }

public:
    bool add(OrderId id, Side side, Price price, Qty qty) {
        if (qty <= 0 || orders_.count(id)) return false;
        auto pos = on(side, [&](auto& book) {
            Level& lvl = book[price];
            lvl.total += qty;
            lvl.queue.push_back({id, qty});
            return std::prev(lvl.queue.end());
        });
        orders_.emplace(id, Loc{side, price, pos});
        return true;
    }

    bool cancel(OrderId id) {
        auto it = orders_.find(id);
        if (it == orders_.end()) return false;
        remove(it);
        return true;
    }

    bool modify(OrderId id, Qty new_qty) {
        auto it = orders_.find(id);
        if (it == orders_.end() || new_qty < 0) return false;
        const Loc loc = it->second;
        if (new_qty == 0) {
            remove(it);
        } else if (new_qty <= loc.pos->qty) {  // reduce in place: keeps time priority
            on(loc.side, [&](auto& book) { return book.find(loc.price)->second.total -= loc.pos->qty - new_qty; });
            loc.pos->qty = new_qty;
        } else {                               // increase: back of the queue
            remove(it);
            add(id, loc.side, loc.price, new_qty);
        }
        return true;
    }

    std::optional<std::pair<Price, Qty>> best_bid() const { return best(bids_); }
    std::optional<std::pair<Price, Qty>> best_ask() const { return best(asks_); }

    std::vector<std::pair<Price, Qty>> depth(Side side, std::size_t n) const {
        return on(side, [&](const auto& book) {
            std::vector<std::pair<Price, Qty>> out;
            for (auto it = book.begin(); it != book.end() && out.size() < n; ++it)
                out.emplace_back(it->first, it->second.total);
            return out;
        });
    }

    Qty volume_at(Side side, Price price) const {
        return on(side, [&](const auto& book) {
            auto it = book.find(price);
            return it == book.end() ? Qty{0} : it->second.total;
        });
    }

    std::vector<OrderId> queue_at(Side side, Price price) const {
        return on(side, [&](const auto& book) {
            std::vector<OrderId> out;
            if (auto it = book.find(price); it != book.end())
                for (const auto& r : it->second.queue) out.push_back(r.id);
            return out;
        });
    }

    std::size_t order_count() const { return orders_.size(); }

private:
    template <class Book> static std::optional<std::pair<Price, Qty>> best(const Book& book) {
        if (book.empty()) return std::nullopt;
        return std::pair{book.begin()->first, book.begin()->second.total};
    }

    void remove(std::unordered_map<OrderId, Loc>::iterator it) {
        const Loc loc = it->second;
        on(loc.side, [&](auto& book) {
            auto lvl = book.find(loc.price);
            lvl->second.total -= loc.pos->qty;
            lvl->second.queue.erase(loc.pos);
            if (lvl->second.queue.empty()) book.erase(lvl);
            return 0;
        });
        orders_.erase(it);
    }

    std::map<Price, Level, std::greater<Price>> bids_;
    std::map<Price, Level> asks_;
    std::unordered_map<OrderId, Loc> orders_;
};
```

## Complexity

- Time: `add` O(log P) (map lookup/insert), `cancel` and `modify` O(1) expected for the id lookup plus O(log P) to find the level; `best_*` O(1); `depth` O(n); `volume_at` O(log P); `queue_at` O(log P + k).
- Space: O(number of orders + number of levels).

## Interview follow-ups

- **Latency.** `std::map` and `std::list` allocate a node per level and per order and scatter them over the heap, so every operation is a few cache misses. Real books use pooled order objects (intrusive doubly linked lists, a free list, no `new` on the hot path) and an open-addressing hash map for ids.
- **Price ladder instead of a tree.** If prices live in a known band (e.g. +/- a few thousand ticks around the last trade), use an array indexed by `price - base` and track the best index. Add/cancel become O(1); finding the next best level after the top empties needs a scan or a bitmap of non-empty levels (find-first-set on 64-bit words).
- **Most activity is near the top.** A sorted vector of levels with the best at the back makes insert/erase near the top cheap (few elements to shift) and is very cache friendly; many HFT books do exactly this.
- **Order book feeds.** Exchanges publish this book as L3 (every order: add/modify/delete by id, which is what you just built), L2 (aggregated quantity per level) or L1 (top of book only).
- **Modify rules differ** by venue: some also make price changes or any modify lose priority; some allow "reduce only" messages. Always check the venue spec.
