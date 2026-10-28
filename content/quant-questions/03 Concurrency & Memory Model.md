---
topic: "Concurrency & Memory Model"
---
# Concurrency & Memory Model

Threads, locks, atomics and the C++ memory model.

## Data race or race condition · Easy

What is the difference between a data race and a race condition?

### Answer

**A data race is a specific language-level bug: two threads access the same memory location without synchronisation, at least one writes, and at least one access is non-atomic — it is undefined behaviour in C++. A race condition is a logic bug where the result depends on timing.** You can have a race condition with no data race (two atomic operations in a check-then-act sequence) and a data race that happens to "work". Fixing data races with atomics does not automatically fix race conditions.

## Mutex or binary semaphore · Easy

How does a mutex differ from a binary semaphore?

### Answer

**A mutex has ownership; a semaphore does not.** Only the thread that locked a mutex may unlock it, which enables priority inheritance and recursive variants. A semaphore is just a counter: any thread may `release` it, which makes it suitable for signalling between threads (e.g. producer tells consumer) rather than protecting a critical section.

## Deadlock versus livelock · Easy

Distinguish deadlock and livelock.

### Answer

**Deadlock: threads are blocked forever, each waiting for a resource another holds. Livelock: threads keep running and reacting to each other but make no progress** (e.g. both back off and retry in lockstep). Deadlock requires mutual exclusion, hold-and-wait, no preemption and a circular wait; livelock is usually cured with randomised backoff.

## Preventing deadlock · Medium

```cpp
void transfer(Account& a, Account& b, int amt) {
    std::lock_guard la(a.m);
    std::lock_guard lb(b.m);
    a.balance -= amt; b.balance += amt;
}
```

How can this deadlock, and how do you fix it?

### Answer

**`transfer(x, y)` and `transfer(y, x)` running concurrently each take one lock and wait for the other.** Fix by breaking the circular wait: lock both at once with `std::scoped_lock lk(a.m, b.m);`, which uses a deadlock-avoidance algorithm, or always acquire locks in a global order (e.g. by account id or address). Also handle `&a == &b`, since locking the same non-recursive mutex twice is UB.

## When a spinlock wins · Medium

When is a spinlock preferable to a blocking mutex?

### Answer

**When critical sections are very short, contention is low, and threads are pinned to dedicated cores** — common on trading hot paths. Spinning avoids the syscall and context-switch cost (microseconds) of sleeping. It is a bad choice when the holder can be preempted or when threads outnumber cores, because spinners burn CPU while the holder cannot run. Spin with a relaxed load (test-and-test-and-set) and a pause instruction to reduce cache-line traffic.

## Why the predicate? · Medium

```cpp
std::unique_lock lk(m);
cv.wait(lk);
process(queue.front());
```

What is wrong, and how should it be written?

### Answer

**`wait` can return without a matching notification (spurious wakeup), and a notification sent before `wait` started is lost.** In either case the queue may be empty. Always wait on a condition over shared state: `cv.wait(lk, [&]{ return !queue.empty(); });`, which loops re-checking the predicate under the lock. The producer must modify that state while holding the same mutex.

## Thread-safe versus reentrant · Medium

What is the difference between a thread-safe function and a reentrant one?

### Answer

**Thread-safe: correct when called concurrently from multiple threads, possibly using locks. Reentrant: correct if re-entered before a previous call finishes on the same thread** (via recursion or a signal handler), which typically means no shared or static state at all. A function that takes a mutex is thread-safe but not reentrant: a signal handler calling it while it holds the lock deadlocks. `strtok` is neither; `strtok_r` is reentrant.

## What std::atomic guarantees · Easy

What does wrapping an `int` in `std::atomic<int>` guarantee?

### Answer

**Each operation on it is indivisible (no torn reads/writes) and does not constitute a data race; by default operations are sequentially consistent.** Read-modify-write ops like `fetch_add` are single atomic steps. It does not make sequences of operations atomic: `if (x == 0) x = 1;` is still a race condition. Atomics for larger types may use a hidden lock; check `is_always_lock_free`.

## Relaxed message passing · Medium

```cpp
int data = 0;
std::atomic<bool> ready{false};

// Thread 1
data = 42;
ready.store(true, std::memory_order_relaxed);

// Thread 2
while (!ready.load(std::memory_order_relaxed)) {}
assert(data == 42);
```

Can the assert fire?

### Answer

**Yes — and worse, it is a data race (UB) on `data`.** Relaxed operations are atomic but impose no ordering on other memory, so thread 2 can see `ready == true` before the write to `data` is visible (on ARM this really happens). Fix with `store(true, std::memory_order_release)` paired with `load(std::memory_order_acquire)`.

## Release meets acquire · Medium

Same as before, but thread 1 uses `ready.store(true, std::memory_order_release)` and thread 2 uses `ready.load(std::memory_order_acquire)`. Can the assert fire?

### Answer

**No.** When the acquire load reads the value written by the release store, the store *synchronises-with* the load: everything thread 1 wrote before the release happens-before everything thread 2 does after the acquire. So `data == 42` is guaranteed and there is no data race. On x86 these compile to plain moves; on ARM they become `stlr`/`ldar`.

## Store buffering · Hard

```cpp
std::atomic<int> x{0}, y{0};
int r1, r2;
// Thread 1                       // Thread 2
x.store(1, std::memory_order_release);   y.store(1, std::memory_order_release);
r1 = y.load(std::memory_order_acquire);  r2 = x.load(std::memory_order_acquire);
```

After both threads finish, can `r1 == 0 && r2 == 0`?

### Answer

**Yes.** Acquire/release only orders operations around a synchronising pair; it does not stop a store from being reordered after a later load to a different location. Even x86 allows this (store buffers). Only `memory_order_seq_cst` on all four operations (or seq_cst fences between store and load) forbids it, because seq_cst requires a single total order consistent with each thread's program order.

## compare_exchange weak or strong · Medium

What is the difference between `compare_exchange_weak` and `compare_exchange_strong`, and when do you use each?

### Answer

**`weak` may fail spuriously even when the value equals `expected`; `strong` fails only when the value really differs.** On LL/SC architectures (ARM, POWER) `weak` maps to a single LL/SC attempt, while `strong` needs an internal retry loop. Use `weak` inside a loop that retries anyway (most CAS loops); use `strong` for one-shot attempts where a spurious failure would be wrong or costly. On failure, both write the current value into `expected`.

## ABA problem in lock-free code · Hard

A lock-free stack pops with: read `head` as `A`, read `next = A->next`, then `CAS(head, A, next)`. What is the ABA problem here?

### Answer

**Between the read and the CAS, another thread pops `A`, pops `B`, and pushes `A` back (same address, possibly reused memory). The CAS still sees `A` and succeeds, installing the stale `next` (`B`, now freed), corrupting the stack.** CAS checks the value, not whether it changed in between. Fixes: tagged pointers / version counters (double-width CAS), hazard pointers, epoch-based reclamation, or never reusing nodes while readers may hold them.

## Lock-free versus wait-free · Medium

Define lock-free and wait-free.

### Answer

**Lock-free: some thread always makes progress in a finite number of steps, even if others are suspended — the system as a whole never stalls, but individual threads can starve. Wait-free: every thread completes its operation in a bounded number of its own steps.** A CAS retry loop is lock-free but not wait-free. `fetch_add` on hardware with an atomic add instruction is wait-free. Obstruction-free is the weaker level below lock-free.

## False sharing · Medium

```cpp
struct Counters { std::atomic<long> a; std::atomic<long> b; };
```

Thread 1 increments only `a`, thread 2 only `b`. Why is this slow, and how do you fix it?

### Answer

**False sharing: `a` and `b` sit on the same 64-byte cache line, so each write invalidates the other core's copy and the line ping-pongs between cores**, even though the threads never touch the same variable. Pad them apart: `alignas(64) std::atomic<long> a; alignas(64) std::atomic<long> b;` or use `std::hardware_destructive_interference_size`. On some Intel CPUs the adjacent-line prefetcher makes 128 bytes safer.

## volatile is not for threads · Easy

Can `volatile bool stop;` be used as a stop flag between threads in C++?

### Answer

**No.** `volatile` only stops the compiler from eliding or merging accesses (meant for memory-mapped I/O); it provides no atomicity and no inter-thread ordering, so concurrent access is still a data race and UB. Use `std::atomic<bool>`. (MSVC's old extension giving `volatile` acquire/release semantics is non-standard.)

## Double-checked locking · Hard

```cpp
Widget* instance = nullptr;
std::mutex m;
Widget* get() {
    if (!instance) {
        std::lock_guard lk(m);
        if (!instance) instance = new Widget();
    }
    return instance;
}
```

What is wrong, and how do you fix it?

### Answer

**The unlocked first read of `instance` races with the write inside the lock (UB), and a reader can see a non-null pointer before the `Widget`'s fields are visible.** Make `instance` a `std::atomic<Widget*>`, load with `acquire` and store with `release` after construction. Simpler: use a function-local static or `std::call_once`, which do this correctly for you.

## Meyers singleton · Easy

```cpp
Logger& logger() { static Logger l; return l; }
```

Is the initialisation thread-safe? What does it cost per call?

### Answer

**Yes, since C++11** ("magic statics"): if several threads call it concurrently, exactly one constructs `l` and the others block until it finishes. After initialisation, each call costs a check of a guard flag (an acquire load and branch), which is cheap but not free on a hot path. Destruction happens at exit in reverse order, which can bite if another static's destructor uses the logger.

## std::call_once · Easy

What does `std::call_once` provide, and what happens if the callable throws?

### Answer

**It runs the callable exactly once across all threads that call it with the same `std::once_flag`; other callers wait until that call completes and then see its effects.** If the callable throws, the exception propagates to that caller, the flag is not set, and another caller will attempt the call again. It is the general-purpose alternative to a function-local static.

## Sizing a thread pool · Medium

How many threads should a thread pool have?

### Answer

**For CPU-bound work, about the number of hardware cores (`std::thread::hardware_concurrency()`); for work that blocks, more — roughly cores × (1 + wait time / compute time).** Extra CPU-bound threads only add context switches and cache thrashing. In low-latency systems, hot threads are pinned one per isolated core and never oversubscribed; blocking I/O is moved to separate threads.

## std::async launch policies · Medium

```cpp
auto f = std::async(compute);
```

Is `compute` guaranteed to run on another thread? What pitfall exists with the returned future?

### Answer

**No.** The default policy is `std::launch::async | std::launch::deferred`, so the implementation may defer it and run it lazily on the thread that calls `get()`/`wait()` — or never, if nobody does. Pass `std::launch::async` to force a new thread. Pitfall: the destructor of a future returned by `std::async` (async policy) blocks until the task finishes, so `std::async(std::launch::async, task);` without keeping the future runs synchronously.

## Cost of copying a shared_ptr · Medium

Why can passing `std::shared_ptr<T>` by value be costly in multithreaded code?

### Answer

**Each copy and destruction performs an atomic increment/decrement on the control block's reference count.** Atomic RMWs cost tens of cycles uncontended, and when many threads copy the same pointer the control block's cache line bounces between cores. Pass `const std::shared_ptr<T>&` or a plain `T&`/`T*` when the callee does not take ownership; move it when it does.

## yield or sleep_for · Easy

What is the difference between `std::this_thread::yield()` and `std::this_thread::sleep_for(0ms)` / `sleep_for(1us)`?

### Answer

**`yield` hints to the scheduler to run another ready thread, returning immediately if there is none; `sleep_for` blocks the thread for at least the given duration.** Sleep granularity depends on the OS timer, so `sleep_for(1us)` often sleeps 50 µs or more. In a busy-wait loop, `yield` keeps latency low but still uses the core; sleeping saves CPU at the cost of wake-up latency.

## Priority inversion · Medium

What is priority inversion and how is it mitigated?

### Answer

**A high-priority thread waits for a lock held by a low-priority thread, while a medium-priority thread preempts the low one, so the high-priority thread is effectively blocked by the medium one.** Mitigations: priority inheritance (the lock holder temporarily inherits the waiter's priority, e.g. `PTHREAD_PRIO_INHERIT`), priority ceiling, or avoiding shared locks between priority levels altogether (lock-free queues). It famously hit the Mars Pathfinder rover.

## Counter with fetch_add · Easy

```cpp
std::atomic<int> c{0};
auto work = [&] { for (int i = 0; i < 100000; ++i) c.fetch_add(1, std::memory_order_relaxed); };
std::thread t1(work), t2(work);
t1.join(); t2.join();
std::cout << c << '\n';
```

What is printed? Is `relaxed` safe here?

### Answer

`200000`, **and yes, relaxed is fine.** Every RMW on one atomic is part of a single modification order, so no increments are lost regardless of memory order. Ordering only matters when other memory must be published alongside the counter; `join()` already synchronises the final read. Replacing `fetch_add` with `c = c + 1` would lose updates.
