---
topic: "Trading Systems"
difficulty: Medium
---
# Per-Client Order Throttle

**Topic:** Trading Systems · **Difficulty:** Medium

## Problem

Exchanges cap how many messages (new orders, cancels, modifies) each participant may send, for example "at most 100 messages in any 1-second window". A trading firm runs the same check on its own side, in the order gateway, so that a runaway strategy is stopped before the exchange disconnects the whole firm. This is a **sliding window** limit: at every moment, look back exactly `W` nanoseconds.

Implement a throttle shared by many clients:

```cpp
class Throttler {
public:
    // At most max_msgs accepted messages per client in any window of window_ns nanoseconds.
    Throttler(std::size_t max_msgs, std::uint64_t window_ns);

    // A message from client_id at time ts_ns. Returns true and records it if the client has
    // fewer than max_msgs ACCEPTED messages with timestamp t where ts_ns - t < window_ns.
    // Otherwise returns false; a rejected message is not recorded and does not count later.
    bool allow(std::uint64_t client_id, std::uint64_t ts_ns);
};
```

So a message accepted at time `t` stops counting at time `t + window_ns` exactly. Timestamps passed to `allow` never decrease from one call to the next (across all clients). Clients are independent of each other.

## Examples

**Example 1**
```cpp
Throttler t(2, 100);    // 2 messages per 100 ns
t.allow(7, 0);          // true
t.allow(7, 10);         // true
t.allow(7, 50);         // false: 2 already in (−50, 50]
t.allow(7, 99);         // false: still 2 in the window
t.allow(7, 100);        // true: the message at 0 has expired
t.allow(7, 105);        // false: messages at 10 and 100 are in the window
```

**Example 2**
```cpp
Throttler t(1, 1000);
t.allow(1, 5);          // true
t.allow(2, 5);          // true: a different client has its own budget
t.allow(1, 6);          // false
```

## Constraints

- `1 <= max_msgs <= 10^5`, `1 <= window_ns <= 10^12`, timestamps up to `10^18`.
- Up to `10^6` calls and `10^5` distinct clients.
- `allow` in O(1) amortized time. Memory O(max_msgs) per active client at most.
