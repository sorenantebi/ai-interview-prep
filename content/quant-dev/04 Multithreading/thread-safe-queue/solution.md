---
topic: "Multithreading"
difficulty: Medium
---
# Thread-Safe Queue with Close - Solution

## Intuition

One mutex guards a `std::deque` and a `closed_` flag. A consumer that finds nothing to do waits on a condition variable with a predicate, "there is an item, or the queue is closed". Producers notify one waiter per push; `close()` notifies all of them, because every waiter has to re-check and leave.

## Approach

1. `push`: lock, reject if closed, append, unlock, `notify_one()`.
2. `pop`: lock with `std::unique_lock`, `cv.wait(lock, [&]{ return !q.empty() || closed; })`. The predicate form handles spurious wake-ups and the case where the item arrived before we started waiting. If the deque is still empty, the queue is closed and drained: return `nullopt`. Otherwise move the front out.
3. `try_pop`: same, without waiting.
4. `close`: set the flag under the lock, then `notify_all()`.

Notifying after releasing the lock avoids waking a thread that immediately blocks on the mutex we still hold.

## Code

```cpp
#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>
#include <utility>

template <class T>
class ThreadSafeQueue {
public:
    bool push(T value) {
        {
            std::lock_guard<std::mutex> lk(m_);
            if (closed_) return false;
            q_.push_back(std::move(value));
        }
        cv_.notify_one();
        return true;
    }

    std::optional<T> pop() {
        std::unique_lock<std::mutex> lk(m_);
        cv_.wait(lk, [&] { return !q_.empty() || closed_; });
        return take();
    }

    std::optional<T> try_pop() {
        std::lock_guard<std::mutex> lk(m_);
        return take();
    }

    void close() {
        {
            std::lock_guard<std::mutex> lk(m_);
            closed_ = true;
        }
        cv_.notify_all();
    }

    bool closed() const {
        std::lock_guard<std::mutex> lk(m_);
        return closed_;
    }

    std::size_t size() const {
        std::lock_guard<std::mutex> lk(m_);
        return q_.size();
    }

private:
    std::optional<T> take() {  // caller holds m_
        if (q_.empty()) return std::nullopt;
        std::optional<T> v(std::move(q_.front()));
        q_.pop_front();
        return v;
    }

    mutable std::mutex m_;
    std::condition_variable cv_;
    std::deque<T> q_;
    bool closed_ = false;
};
```

## Complexity

- Time: O(1) amortised per operation, plus lock contention.
- Space: O(number of queued items).

## Interview follow-ups

- Why must the wait use a predicate (or a `while` loop)? Spurious wake-ups, and "stolen" items when two consumers wake for one push.
- `notify_one` inside or outside the lock: correctness vs. an extra context switch.
- Why is `std::queue::front()` + `pop()` a bad public API for a concurrent queue? (The check-then-act race; return the value from `pop`.)
- The mutex is a contention point: how would you shard it, batch pops (`pop_all` swapping the deque), or move to a lock-free MPMC queue?
- What if `T`'s move constructor throws inside `pop`? (The item must not be lost.)
