---
topic: "Lock-free & Atomics"
difficulty: Hard
---
# Lock-Free Treiber Stack - Solution

## Intuition

The whole stack state is one pointer, `head_`. Any change is "read head, build the new head, CAS it in if head has not changed meanwhile":

- **push**: the new node's `next` is the current head; CAS `head_` from that value to the new node.
- **pop**: read head `h`; CAS `head_` from `h` to `h->next`. The thread whose CAS succeeds owns `h` exclusively and may move the value out.

Because `compare_exchange_weak` writes the current value back into `expected` on failure, each retry starts from fresh data.

## Approach

1. `Node { T value; Node* next; Node* retired_next; }`. `next` is written only before the node is published, so concurrent poppers may read it safely.
2. `push`: allocate the node, `n->next = head_.load(relaxed)`, loop `head_.compare_exchange_weak(n->next, n, release, relaxed)`. The release publishes `value` and `next` to whoever later acquires the node.
3. `pop`: `h = head_.load(acquire)`; loop `while (h && !head_.compare_exchange_weak(h, h->next, acquire, acquire))`. If `h` is null, return `nullopt`. Otherwise move `h->value` out and **retire** `h`.
4. `retire`: push `h` onto a second lock-free list `retired_` via its `retired_next` field (a separate field, so it never races with poppers still reading `h->next`).
5. Destructor: delete every node on the stack and on the retired list.

### Why this is safe: ABA and use-after-free

Two classic bugs break a naive Treiber stack that `delete`s in `pop`:

- **Use-after-free.** Thread A reads `h = head_` and is about to read `h->next`. Thread B pops `h` and deletes it. A now dereferences freed memory.
- **ABA.** A reads `h` and `h->next == x`, then stalls. B pops `h`, pops `x`, deletes `h`, and a new push gets the **same address** back from the allocator, so `head_ == h` again. A's CAS (`h` -> `x`) succeeds, installing the freed `x` as head: the stack is corrupted.

Never freeing a popped node while the stack is alive removes both: memory stays valid, and since nodes are never reused, an address cannot come back to `head_` once it has left. The price is memory that grows with the number of pops, which is fine here but not for a long-running process. Production options:

- **Hazard pointers**: each thread publishes the node it is about to dereference; a retired node is freed only when no hazard pointer points at it (C++26 `std::hazard_pointer`).
- **Epoch-based reclamation / RCU**: threads announce the epoch they run in; a node retired in epoch *e* is freed once every thread has moved past *e*.
- **Tagged pointers**: pair the pointer with a counter in a double-width CAS (or spare pointer bits) so a recycled address no longer compares equal. This fixes ABA, not use-after-free, so it suits node pools that never return memory to the OS.

## Code

```cpp
#include <atomic>
#include <optional>
#include <utility>

template <class T>
class LockFreeStack {
    struct Node {
        T value;
        Node* next;
        Node* retired_next = nullptr;
    };

public:
    LockFreeStack() = default;
    LockFreeStack(const LockFreeStack&) = delete;
    LockFreeStack& operator=(const LockFreeStack&) = delete;

    ~LockFreeStack() {
        free_list(head_.load(std::memory_order_relaxed), &Node::next);
        free_list(retired_.load(std::memory_order_relaxed), &Node::retired_next);
    }

    void push(T value) {
        Node* n = new Node{std::move(value), head_.load(std::memory_order_relaxed)};
        while (!head_.compare_exchange_weak(n->next, n, std::memory_order_release,
                                            std::memory_order_relaxed)) {
        }
    }

    std::optional<T> pop() {
        Node* h = head_.load(std::memory_order_acquire);
        while (h && !head_.compare_exchange_weak(h, h->next, std::memory_order_acquire,
                                                 std::memory_order_acquire)) {
        }
        if (!h) return std::nullopt;
        std::optional<T> out(std::move(h->value));  // we own h now
        retire(h);
        return out;
    }

    bool empty() const { return head_.load(std::memory_order_acquire) == nullptr; }

private:
    // Popped nodes are kept until the destructor (no use-after-free, no ABA); see the reclamation notes above.
    void retire(Node* n) {
        n->retired_next = retired_.load(std::memory_order_relaxed);
        while (!retired_.compare_exchange_weak(n->retired_next, n, std::memory_order_release,
                                               std::memory_order_relaxed)) {
        }
    }

    static void free_list(Node* n, Node* Node::*link) {
        while (n) {
            Node* next = n->*link;
            delete n;
            n = next;
        }
    }

    std::atomic<Node*> head_{nullptr};
    std::atomic<Node*> retired_{nullptr};
};
```

## Complexity

- Time: O(1) per operation without contention; under contention a CAS can fail and retry, but each failure means another thread succeeded (lock-free).
- Space: O(total pushes) until destruction, because retired nodes are kept.

## Interview follow-ups

- Walk through the ABA interleaving step by step, and explain why a tagged pointer fixes it but a hazard pointer fixes more.
- Every operation CASes the same `head_` cache line: why can this be *slower* than a mutex under heavy contention? (Elimination back-off, per-thread caches.)
- `memory_order` choices: why does `push` need release and `pop` acquire, and could `pop`'s failure order be relaxed?
- Is `std::atomic<Node*>` always lock-free? What about a 16-byte {pointer, tag} struct (`cmpxchg16b`, `is_always_lock_free`)?
- Make `pop` exception-safe for a `T` whose move constructor throws.
- Lock-free vs wait-free: is this stack wait-free? (No: a thread can retry forever while others keep winning.)
