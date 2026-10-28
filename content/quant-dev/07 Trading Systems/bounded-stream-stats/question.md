---
topic: "Trading Systems"
difficulty: Medium
---
# Statistics of a Bounded Integer Stream

**Topic:** Trading Systems · **Difficulty:** Medium

## Problem

Many values in a trading system are small integers that arrive millions of times a day: the spread in ticks, the size of a trade in lots, a latency measurement in microseconds bucketed to a cap. Monitoring wants their median, most common value and percentiles (e.g. "99th percentile tick-to-trade latency"), and storing or sorting every sample is wasteful when the values can only take about a thousand different values.

Implement a stream summary for integers in a fixed range `[lo, hi]`:

```cpp
class BoundedStats {
public:
    BoundedStats(int lo, int hi);  // lo <= hi, hi - lo <= 1000

    void add(int x);               // throws std::out_of_range if x is outside [lo, hi]
    std::uint64_t count() const;   // number of values added

    // Nearest-rank percentile, 0 <= p <= 100: with n values sorted ascending,
    // return the k-th smallest (1-based), where k = max(1, ceil(p * n / 100)).
    std::optional<int> percentile(double p) const;

    // Middle value for odd n; the average of the two middle values for even n.
    std::optional<double> median() const;

    // Most frequent value; the smallest one if several tie.
    std::optional<int> mode() const;
};
```

All queries return `std::nullopt` while the stream is empty.

## Examples

**Example 1**
```cpp
BoundedStats s(0, 10);
for (int x : {3, 1, 4, 1, 5, 9, 2, 6}) s.add(x);
s.count();            // 8
s.median();           // sorted 1 1 2 3 4 5 6 9 -> (3 + 4) / 2 = 3.5
s.mode();             // 1
s.percentile(25);     // k = 2 -> 1
s.percentile(90);     // k = ceil(7.2) = 8 -> 9
s.percentile(0);      // k = 1 -> 1 (the minimum)
```

**Example 2**
```cpp
BoundedStats s(-5, 5);
s.mode();             // std::nullopt
s.add(-5); s.add(5); s.add(5); s.add(-5);
s.mode();             // -5: tie, smallest wins
s.add(6);             // throws std::out_of_range
```

## Constraints

- Up to `10^9` values in total (use 64-bit counters); `hi - lo <= 1000`.
- `add` in O(1); `mode` in O(1); `median` and `percentile` in O(hi - lo + 1).
- Memory O(hi - lo + 1), independent of how many values were added.
