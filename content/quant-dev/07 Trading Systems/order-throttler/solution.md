---
topic: "Trading Systems"
difficulty: Medium
---
# Per-Client Order Throttle - Solution

## Intuition

For each client keep the timestamps of its accepted messages that are still inside the window, oldest first. On a new message, first drop the timestamps that have aged out (`ts - oldest >= W`); what remains is exactly the set of messages that count. If there are fewer than `N`, accept and append.

Because time only moves forward, a timestamp that has expired never comes back, so each one is appended once and popped at most once: O(1) amortized. And since we never store more than `N` per client, memory is bounded too.

## Approach

1. `std::unordered_map<client, std::deque<uint64_t>>`.
2. `allow(c, ts)`: get the client's deque; pop from the front while `ts - front >= W`.
3. If `size < N`: push `ts`, return true. Else return false (store nothing).

## Code

```cpp
#include <cstddef>
#include <cstdint>
#include <deque>
#include <unordered_map>

class Throttler {
public:
    Throttler(std::size_t max_msgs, std::uint64_t window_ns) : max_(max_msgs), window_(window_ns) {}

    bool allow(std::uint64_t client_id, std::uint64_t ts_ns) {
        std::deque<std::uint64_t>& sent = clients_[client_id];
        while (!sent.empty() && ts_ns - sent.front() >= window_) sent.pop_front();
        if (sent.size() >= max_) return false;
        sent.push_back(ts_ns);
        return true;
    }

private:
    std::size_t max_;
    std::uint64_t window_;
    std::unordered_map<std::uint64_t, std::deque<std::uint64_t>> clients_;
};
```

## Complexity

- Time: O(1) amortized per call (each accepted timestamp is pushed and popped once) plus the expected O(1) hash lookup.
- Space: O(max_msgs) per client.

## Interview follow-ups

- **Fixed memory, no allocation.** Since a client never holds more than `N` timestamps, use a ring buffer of exactly `N` slots: the slot you are about to overwrite is the oldest, so the check is just "is `ts - ring[head] >= W`?". O(1) worst case, not just amortized.
- **Cheaper approximations.** A token bucket (refill `N/W` tokens per ns, capacity `N`) needs two numbers per client and allows smooth bursts; a fixed-window counter is cheapest but can let `2N` messages through around a window boundary. Know which one your exchange actually enforces.
- **Where to put it.** In the order gateway, after risk checks and before the socket write; rejected messages should go back to the strategy as an internal reject, never to the exchange.
- **Clock source.** Use a monotonic clock (or the NIC hardware timestamp), never wall-clock time that can jump backwards.
- **Many clients, hot path.** Replace `std::unordered_map` with a flat array indexed by a small session id assigned at login.
