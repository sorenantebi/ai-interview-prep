---
topic: "Trading Systems"
difficulty: Medium
---
# Top of Book from an L2 Feed

**Topic:** Trading Systems · **Difficulty:** Medium

## Problem

Exchanges publish **L2 market data**: instead of every individual order, they send the total quantity resting at each price level. An update says "on the bid (buy) side, the level at price `p` now has total quantity `q`"; `q = 0` means the level is gone. A trading system rebuilds the book from these updates and mostly cares about the **top of book**:

- **best bid**: highest bid price (and its quantity), **best ask**: lowest ask price (and its quantity);
- **spread** = best ask - best bid (in ticks), normally positive;
- **mid price** = (best bid + best ask) / 2, a common "fair value" reference.

In a healthy book the best bid is strictly below the best ask. If `best bid >= best ask` the book is **crossed** (or **locked** when equal). On a real exchange that can't last, so seeing it usually means a missed or out-of-order packet: strategies must stop trading on that book until it is consistent again. Your feed handler must flag it, not hide it.

Implement:

```cpp
enum class Side { Bid, Ask };

struct Quote {
    std::optional<std::pair<std::int64_t, std::int64_t>> bid;  // (price, qty) of the best bid
    std::optional<std::pair<std::int64_t, std::int64_t>> ask;  // (price, qty) of the best ask
    std::optional<std::int64_t> spread;                         // ask - bid, when both sides exist
    bool crossed = false;                                       // both exist and bid >= ask
    bool operator==(const Quote&) const = default;
};

class TopOfBook {
public:
    // Sets the total quantity of one level (0 removes it; removing a missing level is a no-op)
    // and returns the top of book after the update. Throws std::invalid_argument if new_qty < 0.
    Quote apply(Side side, std::int64_t price, std::int64_t new_qty);

    Quote quote() const;              // current top of book
    std::optional<double> mid() const;  // (best bid + best ask) / 2, or nullopt if a side is empty
};
```

## Examples

**Example 1**
```cpp
TopOfBook b;
b.apply(Side::Bid, 100, 5);   // bid (100,5), no ask, no spread, not crossed
b.apply(Side::Ask, 103, 2);   // bid (100,5), ask (103,2), spread 3
b.apply(Side::Bid, 101, 1);   // bid (101,1), ask (103,2), spread 2
b.mid();                      // 102.0
b.apply(Side::Bid, 101, 0);   // level removed: bid (100,5), spread 3
b.apply(Side::Ask, 103, 9);   // same level, new size: ask (103,9)
```

**Example 2**
```cpp
TopOfBook b;
b.apply(Side::Ask, 50, 1);
b.apply(Side::Bid, 50, 4);    // bid (50,4), ask (50,1), spread 0, crossed = true
b.apply(Side::Ask, 50, 0);    // ask gone: bid (50,4), no spread, crossed = false
b.apply(Side::Bid, 49, -1);   // throws std::invalid_argument
```

## Constraints

- Up to `10^6` updates over up to `10^5` levels per side; prices are arbitrary `int64` ticks.
- `apply` in O(log P); `quote` and `mid` in O(1).
