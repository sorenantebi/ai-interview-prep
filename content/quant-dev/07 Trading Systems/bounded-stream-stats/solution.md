---
topic: "Trading Systems"
difficulty: Medium
---
# Statistics of a Bounded Integer Stream - Solution

## Intuition

When the values come from a small range, a **histogram is the data**: `count[x - lo]` loses nothing about the multiset, because the order of arrival doesn't matter for median, mode or percentiles. Adding is one increment. Any order statistic ("the k-th smallest") is a walk over at most ~1001 buckets, accumulating counts until the running total reaches `k`.

The mode can even be kept up to date on every `add`: only the bucket that just grew can become the new mode.

## Approach

1. `counts_` = vector of `hi - lo + 1` 64-bit counters, `n_` = total.
2. `add(x)`: range check, `++counts_[x - lo]`, `++n_`; if that bucket now beats the current mode's count, or ties it with a smaller value, it becomes the mode.
3. `kth(k)` (1-based): walk the buckets, adding counts until the sum reaches `k`; return `lo + i`.
4. `percentile(p)`: `k = max(1, ceil(p * n / 100))`, return `kth(k)`.
5. `median()`: `kth((n + 1) / 2)` and `kth(n / 2 + 1)`; for odd `n` both are the middle element, for even `n` they are the two middle ones, so return their average either way.

## Code

```cpp
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <optional>
#include <stdexcept>
#include <vector>

class BoundedStats {
public:
    BoundedStats(int lo, int hi) : lo_(lo), hi_(hi), counts_(static_cast<std::size_t>(hi - lo) + 1, 0) {}

    void add(int x) {
        if (x < lo_ || x > hi_) throw std::out_of_range("value outside [lo, hi]");
        const std::size_t i = static_cast<std::size_t>(x - lo_);
        ++counts_[i];
        ++n_;
        if (counts_[i] > counts_[mode_] || (counts_[i] == counts_[mode_] && i < mode_)) mode_ = i;
    }

    std::uint64_t count() const { return n_; }

    std::optional<int> percentile(double p) const {
        if (n_ == 0) return std::nullopt;
        const double rank = std::ceil(p * static_cast<double>(n_) / 100.0);
        return kth(std::max<std::uint64_t>(1, static_cast<std::uint64_t>(rank)));
    }

    std::optional<double> median() const {
        if (n_ == 0) return std::nullopt;
        return (kth((n_ + 1) / 2) + static_cast<double>(kth(n_ / 2 + 1))) / 2.0;
    }

    std::optional<int> mode() const {
        if (n_ == 0) return std::nullopt;
        return lo_ + static_cast<int>(mode_);
    }

private:
    // k-th smallest value, 1 <= k <= n_.
    int kth(std::uint64_t k) const {
        std::uint64_t seen = 0;
        for (std::size_t i = 0; i < counts_.size(); ++i) {
            seen += counts_[i];
            if (seen >= k) return lo_ + static_cast<int>(i);
        }
        return lo_ + static_cast<int>(counts_.size()) - 1;  // k > n_ can't happen; keep the compiler happy
    }

    int lo_, hi_;
    std::vector<std::uint64_t> counts_;
    std::uint64_t n_ = 0;
    std::size_t mode_ = 0;
};
```

## Complexity

- Time: `add` and `mode` O(1); `percentile` and `median` O(R) with R = `hi - lo + 1` (at most 1001).
- Space: O(R), no matter how many values arrive.

## Interview follow-ups

- **Faster percentiles.** Keep a Fenwick tree over the buckets: `add` becomes O(log R) and the k-th smallest is an O(log R) descent. Or, if percentile queries are frequent and adds rare, keep a prefix-sum array.
- **Unbounded or wide ranges.** Latencies span nanoseconds to seconds: use log-scaled buckets (HdrHistogram style: exact to a few significant digits), or a sketch such as t-digest / DDSketch with a bounded relative error.
- **Sliding windows.** "Median of the last minute": keep one histogram per second in a ring and subtract the expiring one, or decrement on eviction from a queue of raw values.
- **Concurrency.** Several threads can record into per-thread histograms (no sharing, no atomics) that a monitoring thread merges by adding bucket counts.
- **Percentile definitions differ** (nearest rank, linear interpolation, ...). State which one you implement; with millions of samples they barely differ, with ten they do.
