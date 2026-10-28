---
topic: "Multithreading"
difficulty: Medium
---
# Bounded Blocking Queue - Solution

## Intuition

There are two reasons to sleep, so use two condition variables: producers wait on `not_full_`, consumers wait on `not_empty_`. Every successful push makes the queue "not empty" (wake a consumer) and every successful pop makes it "not full" (wake a producer). One mutex guards the storage, so `size() <= capacity` holds at every moment anyone can observe.

## Approach

1. Store items in a `std::deque<T>` plus the fixed `cap_`.
2. `push`: lock, `not_full_.wait(lk, [&]{ return q_.size() < cap_; })`, append, unlock, `not_empty_.notify_one()`.
3. `pop`: lock, `not_empty_.wait(lk, [&]{ return !q_.empty(); })`, move the front out, unlock, `not_full_.notify_one()`.
4. `try_push` / `try_pop`: check the condition under the lock, return `false` / `nullopt` instead of waiting, notify the other side on success.

With a single condition variable you would need `notify_all` (a push could wake another producer instead of a consumer and the wake-up would be lost). Two CVs let `notify_one` be both correct and cheap.

## Code

```cpp
#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>
#include <utility>

template <class T>
class BoundedBlockingQueue {
public:
    explicit BoundedBlockingQueue(std::size_t capacity) : cap_(capacity) {}

    void push(T value) {
        {
            std::unique_lock<std::mutex> lk(m_);
            not_full_.wait(lk, [&] { return q_.size() < cap_; });
            q_.push_back(std::move(value));
        }
        not_empty_.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lk(m_);
        not_empty_.wait(lk, [&] { return !q_.empty(); });
        T v = std::move(q_.front());
        q_.pop_front();
        lk.unlock();
        not_full_.notify_one();
        return v;
    }

    bool try_push(T value) {
        {
            std::lock_guard<std::mutex> lk(m_);
            if (q_.size() >= cap_) return false;
            q_.push_back(std::move(value));
        }
        not_empty_.notify_one();
        return true;
    }

    std::optional<T> try_pop() {
        std::optional<T> v;
        {
            std::lock_guard<std::mutex> lk(m_);
            if (q_.empty()) return std::nullopt;
            v.emplace(std::move(q_.front()));
            q_.pop_front();
        }
        not_full_.notify_one();
        return v;
    }

    std::size_t size() const {
        std::lock_guard<std::mutex> lk(m_);
        return q_.size();
    }
    std::size_t capacity() const { return cap_; }

private:
    const std::size_t cap_;
    mutable std::mutex m_;
    std::condition_variable not_full_, not_empty_;
    std::deque<T> q_;
};
```

## Complexity

- Time: O(1) per operation plus waiting and lock contention.
- Space: O(capacity). A ring buffer (`std::vector` + head index) would avoid the deque's chunk allocations entirely.

## Interview follow-ups

- Why does a single condition variable with `notify_one` risk a lost wake-up here?
- Add `push_for(value, timeout)` with `wait_for` and a predicate: what does it return on timeout?
- Back-pressure policy in a trading system: block, drop newest, drop oldest, or conflate by symbol? Which is right for market data vs. orders?
- Add `close()` like in the unbounded queue: blocked producers must wake up as well as consumers.
- Replace the mutex with a lock-free ring when there is exactly one producer and one consumer (see SPSC queue).
