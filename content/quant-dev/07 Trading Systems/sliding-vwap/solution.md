---
topic: "Trading Systems"
difficulty: Medium
---
# Sliding-Window VWAP - Solution

## Intuition

VWAP is a ratio of two sums, and both sums are easy to maintain incrementally: add a trade's `price * qty` and `qty` when it arrives, subtract them when it leaves the window. Trades leave in the same order they arrived (time only goes forward), so a FIFO queue tells us exactly which ones to subtract.

Keep the sums as integers (prices are ticks) and divide only when asked. Integer sums never drift, unlike a running `double` that has values added and removed millions of times.

## Approach

1. A `std::deque` of `(ts, price, qty)` plus two `int64` sums: `notional = sum(price * qty)` and `volume = sum(qty)`.
2. `on_trade`: push to the back, add to both sums.
3. `vwap(now)`: pop from the front while `now - front.ts >= window`, subtracting from the sums. Then return `nullopt` if `volume == 0`, else `double(notional) / volume`.

## Code

```cpp
#include <cstdint>
#include <deque>
#include <optional>

class SlidingVwap {
public:
    explicit SlidingVwap(std::uint64_t window_ns) : window_(window_ns) {}

    void on_trade(std::uint64_t ts_ns, std::int64_t price, std::int64_t qty) {
        trades_.push_back({ts_ns, price, qty});
        notional_ += price * qty;
        volume_ += qty;
    }

    std::optional<double> vwap(std::uint64_t now_ns) {
        while (!trades_.empty() && now_ns - trades_.front().ts >= window_) {
            notional_ -= trades_.front().price * trades_.front().qty;
            volume_ -= trades_.front().qty;
            trades_.pop_front();
        }
        if (volume_ == 0) return std::nullopt;
        return static_cast<double>(notional_) / static_cast<double>(volume_);
    }

private:
    struct Trade { std::uint64_t ts; std::int64_t price, qty; };
    std::uint64_t window_;
    std::deque<Trade> trades_;
    std::int64_t notional_ = 0, volume_ = 0;
};
```

## Complexity

- Time: `on_trade` O(1); `vwap` O(1) amortized (each trade is popped once).
- Space: O(trades in the window).

## Interview follow-ups

- **Why not `double` sums?** Adding and subtracting floats over millions of updates accumulates rounding error, and after a burst at a very different price the "empty" sum might not return to 0. Integer ticks are exact; if you must use floats, recompute from scratch periodically or use Kahan summation.
- **Bounded memory.** If the trade rate is unbounded, bucket trades into fixed time slots (say 1 ms) in a ring buffer of `window / slot` buckets: memory becomes fixed and the window becomes approximate at slot granularity.
- **Other rolling stats.** The same add/evict pattern gives rolling volume, trade count and TWAP; rolling min/max need a monotonic deque instead.
- **Exponential VWAP.** An exponentially decaying VWAP needs no queue at all: decay both sums by `exp(-dt / tau)` on each update.
- **Which trades count?** Real VWAP benchmarks exclude some prints (odd lots, off-exchange, opening/closing auctions); the filtering is usually more work than the arithmetic.
