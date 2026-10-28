---
topic: "Trading Systems"
difficulty: Medium
---
# FIFO Position & P&L Tracker

**Topic:** Trading Systems · **Difficulty:** Medium

## Problem

Every trading system tracks, per instrument, its **position** (how many units it holds: positive = **long**, negative = **short**, i.e. sold units it does not own) and its **P&L** (profit and loss):

- **Realized P&L** is locked in: it comes from closing (part of) a position. Buy 10 at 100 and sell 4 at 103 and you have realized `4 * (103 - 100) = 12`.
- **Unrealized P&L** is what the still-open position would make if closed at the current **mark** price.

When you close part of a position that was built at several prices, you must decide which units you are closing. Here we use **FIFO**: the oldest open units (**lots**) are closed first. A fill can also go **through zero**: long 5 and sell 8 closes all 5 (realizing P&L) and opens a new short lot of 3 at the fill price.

For a short lot opened at price `e` and closed at price `c`, the P&L is `(e - c) * qty` (you sold high and bought back low).

Implement, with prices as integer ticks:

```cpp
enum class Side { Buy, Sell };

class PositionTracker {
public:
    // A fill of qty > 0 units at price (ticks).
    void on_fill(Side side, std::int64_t price, std::int64_t qty);

    std::int64_t position() const;                         // signed
    std::int64_t realized_pnl() const;                     // total so far, in ticks * units
    std::int64_t unrealized_pnl(std::int64_t mark) const;  // of the open lots at this mark
    std::optional<double> average_cost() const;            // qty-weighted entry price of the
                                                           // open lots; std::nullopt when flat
};
```

## Examples

**Example 1**
```cpp
PositionTracker t;
t.on_fill(Side::Buy, 100, 10);
t.on_fill(Side::Buy, 110, 10);
t.average_cost();          // 105.0
t.on_fill(Side::Sell, 120, 15);   // closes 10 @100 (+200) and 5 @110 (+50)
t.position();              // 5
t.realized_pnl();          // 250
t.unrealized_pnl(108);     // 5 * (108 - 110) = -10
t.average_cost();          // 110.0
```

**Example 2**
```cpp
PositionTracker t;
t.on_fill(Side::Buy, 50, 5);
t.on_fill(Side::Sell, 48, 8);     // closes 5 @50 (-10), opens short 3 @48
t.position();              // -3
t.realized_pnl();          // -10
t.unrealized_pnl(45);      // 3 * (48 - 45) = 9
t.on_fill(Side::Buy, 45, 3);      // covers the short (+9)
t.position();              // 0
t.realized_pnl();          // -1
t.average_cost();          // std::nullopt
```

## Constraints

- Up to `10^6` fills; `1 <= qty <= 10^6`; prices in `[1, 10^7]`; all P&L values fit in `int64`.
- `position`, `realized_pnl`, `unrealized_pnl` and `average_cost` in O(1).
- `on_fill` O(1) amortized (each lot is opened once and fully closed at most once).
