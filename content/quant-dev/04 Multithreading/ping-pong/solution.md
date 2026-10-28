---
topic: "Multithreading"
difficulty: Easy
---
# Ping-Pong Threads - Solution

## Intuition

Make the turn explicit state: a `bool ping_turn` guarded by a mutex. Each thread waits on a condition variable until it is its turn, appends its word, flips the flag and notifies the other one. The predicate in `wait` means it does not matter which thread starts running first, or whether a notification arrives before the other thread is waiting.

## Approach

1. Shared state: `std::string out`, `bool ping_turn = true`, a mutex and a condition variable.
2. A helper `player(word, my_turn)` loops `n` times: `cv.wait(lk, [&]{ return ping_turn == my_turn; })`, append (with a separating space if `out` is not empty), `ping_turn = !ping_turn`, `cv.notify_one()`.
3. Start `player("ping", true)` and `player("pong", false)` on two threads, join both, return `out`.

There are exactly two threads and only one is ever waiting for the other, so `notify_one` is enough. The joins publish `out` to the calling thread.

## Code

```cpp
#include <condition_variable>
#include <mutex>
#include <string>
#include <thread>

std::string play(int n) {
    std::string out;
    bool ping_turn = true;
    std::mutex m;
    std::condition_variable cv;

    auto player = [&](const char* word, bool my_turn) {
        for (int i = 0; i < n; ++i) {
            std::unique_lock<std::mutex> lk(m);
            cv.wait(lk, [&] { return ping_turn == my_turn; });
            if (!out.empty()) out += ' ';
            out += word;
            ping_turn = !ping_turn;
            lk.unlock();
            cv.notify_one();
        }
    };

    std::thread ping(player, "ping", true);
    std::thread pong(player, "pong", false);
    ping.join();
    pong.join();
    return out;
}
```

## Complexity

- Time: O(n) words, but each one costs a context switch (microseconds): this is about correctness, not speed.
- Space: O(n) for the output.

## Interview follow-ups

- Do it with a single `std::atomic<int>` turn counter and spinning (`while (turn.load(std::memory_order_acquire) % 2 != me)`). What memory orders do you need, and why does spinning beat the condition variable on dedicated cores?
- Generalise to K threads printing in round-robin order.
- What goes wrong if you drop the predicate and call `cv.wait(lk)` alone? (A notify sent before the other thread waits is lost: deadlock.)
- C++20 `std::atomic::wait` / `notify_one`: a futex-style alternative without a mutex.
