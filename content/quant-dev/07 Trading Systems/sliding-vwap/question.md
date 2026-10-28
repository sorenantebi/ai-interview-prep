---
topic: "Trading Systems"
difficulty: Medium
---
# Sliding-Window VWAP

**Topic:** Trading Systems · **Difficulty:** Medium

## Problem

**VWAP** (volume-weighted average price) is the average price of the trades in some period, where each trade counts in proportion to its size:

```
VWAP = sum(price_i * qty_i) / sum(qty_i)
```

A trade of 1000 shares moves it much more than a trade of 1 share. Execution algorithms compare their own fills to VWAP, and signals often use a short rolling VWAP (e.g. "the last 5 seconds") as a fair-value estimate.

Implement a rolling VWAP over the last `window_ns` nanoseconds:

```cpp
class SlidingVwap {
public:
    explicit SlidingVwap(std::uint64_t window_ns);

    // A trade printed at time ts_ns. price is in integer ticks, qty > 0.
    void on_trade(std::uint64_t ts_ns, std::int64_t price, std::int64_t qty);

    // VWAP of the trades with now_ns - ts < window_ns, or std::nullopt if there are none.
    std::optional<double> vwap(std::uint64_t now_ns);
};
```

A trade at time `t` is in the window for `now` in `[t, t + window_ns)`. Timestamps never decrease across all calls (both `on_trade` and `vwap`), so once a trade has left the window it never comes back.

## Examples

**Example 1**
```cpp
SlidingVwap v(100);
v.vwap(0);              // std::nullopt: no trades yet
v.on_trade(10, 200, 1);
v.on_trade(20, 100, 3);
v.vwap(20);             // (200*1 + 100*3) / 4 = 125.0
v.vwap(109);            // 125.0: both trades still inside
v.vwap(110);            // 100.0: the trade at 10 has expired
v.vwap(120);            // std::nullopt: everything expired
```

**Example 2**
```cpp
SlidingVwap v(1000);
v.on_trade(0, 101, 2);
v.on_trade(0, 102, 1);
v.vwap(0);              // (202 + 102) / 3 = 101.333...
```

## Constraints

- `1 <= window_ns <= 10^12`, timestamps up to `10^18`, `1 <= price <= 10^7`, `1 <= qty <= 10^5`.
- At most `10^6` trades inside a window, so `sum(price * qty)` fits in `int64`.
- `on_trade` O(1), `vwap` O(1) amortized. Compare results with a tolerance of `1e-9`.
