---
topic: "Trading Systems"
difficulty: Medium
---
# Top of Book from an L2 Feed - Solution

## Intuition

An L2 update is "set this level's quantity", which is just an assignment (or an erase for 0) in a map from price to quantity. Keep one sorted map per side, ordered so that the best price is `begin()`: bids descending, asks ascending. Then the top of book is two `begin()` lookups, and spread, crossed flag and mid all follow from those two levels.

## Approach

1. `std::map<int64, int64, std::greater<>> bids_`, `std::map<int64, int64> asks_`.
2. `apply`: reject a negative quantity; `erase(price)` for 0, otherwise `book[price] = qty`; return `quote()`.
3. `quote()`: fill `bid`/`ask` from `begin()` when non-empty; if both exist, set `spread = ask - bid` and `crossed = bid >= ask`.
4. `mid()`: average of the two best prices, computed as `(bid + ask) / 2.0` in `double`.

## Code

```cpp
#include <cstdint>
#include <functional>
#include <map>
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
    Quote apply(Side side, std::int64_t price, std::int64_t new_qty) {
        if (new_qty < 0) throw std::invalid_argument("negative quantity");
        if (side == Side::Bid) set(bids_, price, new_qty);
        else set(asks_, price, new_qty);
        return quote();
    }

    Quote quote() const {
        Quote q;
        if (!bids_.empty()) q.bid = *bids_.begin();
        if (!asks_.empty()) q.ask = *asks_.begin();
        if (q.bid && q.ask) {
            q.spread = q.ask->first - q.bid->first;
            q.crossed = q.bid->first >= q.ask->first;
        }
        return q;
    }

    std::optional<double> mid() const {
        if (bids_.empty() || asks_.empty()) return std::nullopt;
        return (static_cast<double>(bids_.begin()->first) + static_cast<double>(asks_.begin()->first)) / 2.0;
    }

private:
    template <class Book>
    static void set(Book& book, std::int64_t price, std::int64_t qty) {
        if (qty == 0) book.erase(price);
        else book[price] = qty;
    }

    std::map<std::int64_t, std::int64_t, std::greater<std::int64_t>> bids_;
    std::map<std::int64_t, std::int64_t> asks_;
};
```

## Complexity

- Time: `apply` O(log P); `quote` and `mid` O(1).
- Space: O(number of levels).

## Interview follow-ups

- **Faster books.** Most updates hit the top few levels. A sorted `std::vector` with the best level at the back (so inserting or removing near the top shifts almost nothing) beats a tree in practice; with a known price band, an array indexed by `price - base` is O(1).
- **Sequence numbers and gaps.** Every feed packet has a sequence number. On a gap, mark the book stale, buffer updates, and recover from a snapshot (or the other A/B line) before trading again. A crossed book is a cheap sanity check that often catches a missed packet.
- **Incremental vs. snapshot.** Feeds send incremental updates in real time and periodic full snapshots for recovery; the handler must apply only updates newer than the snapshot's sequence number.
- **Publish only on change.** Downstream strategies care about top-of-book changes: compare the new quote with the previous one and only notify when it differs, and batch all updates from one packet before publishing (a packet may be half-applied otherwise and look crossed).
- **Mid alternatives.** The micro-price weights bid and ask by the opposite side's size: `(bid * ask_qty + ask * bid_qty) / (bid_qty + ask_qty)`; it leans toward the side that is about to be consumed.
