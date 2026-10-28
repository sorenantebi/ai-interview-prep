---
topic: "Multithreading"
difficulty: Hard
---
# Writer-Preferring Read-Write Lock - Solution

## Intuition

The whole lock is three numbers guarded by an internal mutex: how many readers are inside, whether a writer is inside, and how many writers are **waiting**. Writer preference is one extra term in the reader's entry condition: a reader may enter only if no writer is inside *and none is waiting*. A writer announces itself (`++waiting_writers_`) before it starts to wait, so from that moment new readers stop coming in, the active readers drain, and the writer gets its turn.

## Approach

1. `lock_shared`: wait on `readers_cv_` until `!writer_ && waiting_writers_ == 0`, then `++readers_`.
2. `unlock_shared`: `--readers_`; if it hits zero and a writer is waiting, wake one writer.
3. `lock`: `++waiting_writers_`, wait on `writers_cv_` until `!writer_ && readers_ == 0`, then `--waiting_writers_` and `writer_ = true`.
4. `unlock`: `writer_ = false`. If more writers are waiting, wake one of them (readers keep waiting: writer preference); otherwise wake **all** readers, since they can share.
5. The `try_` versions test the same condition and return `false` instead of waiting.

Two condition variables let us wake exactly the right group; with one CV every unlock would have to `notify_all` and let everybody re-check.

## Code

```cpp
#include <condition_variable>
#include <mutex>

class RWLock {
public:
    void lock_shared() {
        std::unique_lock<std::mutex> lk(m_);
        readers_cv_.wait(lk, [&] { return !writer_ && waiting_writers_ == 0; });
        ++readers_;
    }

    bool try_lock_shared() {
        std::lock_guard<std::mutex> lk(m_);
        if (writer_ || waiting_writers_ > 0) return false;
        ++readers_;
        return true;
    }

    void unlock_shared() {
        std::lock_guard<std::mutex> lk(m_);
        if (--readers_ == 0 && waiting_writers_ > 0) writers_cv_.notify_one();
    }

    void lock() {
        std::unique_lock<std::mutex> lk(m_);
        ++waiting_writers_;
        writers_cv_.wait(lk, [&] { return !writer_ && readers_ == 0; });
        --waiting_writers_;
        writer_ = true;
    }

    bool try_lock() {
        std::lock_guard<std::mutex> lk(m_);
        if (writer_ || readers_ > 0) return false;
        writer_ = true;
        return true;
    }

    void unlock() {
        std::lock_guard<std::mutex> lk(m_);
        writer_ = false;
        if (waiting_writers_ > 0) writers_cv_.notify_one();
        else readers_cv_.notify_all();
    }

private:
    std::mutex m_;
    std::condition_variable readers_cv_, writers_cv_;
    int readers_ = 0;
    int waiting_writers_ = 0;
    bool writer_ = false;
};
```

Notifying while holding `m_` is deliberate here: it is simpler to reason about, and the woken thread re-checks its predicate anyway.

## Complexity

- Time: O(1) bookkeeping per call; every acquire still goes through the internal mutex, so this lock only pays off when the read-side critical section is much longer than that.
- Space: O(1).

## Interview follow-ups

- Writer preference can starve **readers** if writers arrive back to back. How would you alternate fairly (phase-fair / ticket-based RW locks)?
- Why is a reader-writer lock often *slower* than a plain mutex for tiny critical sections? (Every reader still writes the shared counter: cache-line ping-pong.)
- For read-mostly data with one writer, compare with a seqlock (readers never write shared memory) or RCU / atomic `shared_ptr` swap.
- How would you support upgrading a read lock to a write lock, and why does a naive upgrade deadlock with two upgraders?
- `std::shared_mutex` makes no fairness guarantee: what do common implementations do?
