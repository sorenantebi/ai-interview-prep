---
topic: "Smart Pointers & RAII"
difficulty: Hard
---
# Implement SharedPtr and WeakPtr with a Shared Control Block

**Topic:** Smart Pointers & RAII · **Difficulty:** Hard

## Problem

An order-routing component keeps a registry of live sessions, but it must not keep a session alive after the session's owner has closed it. The registry holds *weak* references: it can ask "is it still there?" and, if so, briefly get a strong reference to use it. The same pattern breaks ownership cycles (parent and child pointing at each other) and backs observer lists and caches.

Implement `SharedPtr<T>` and `WeakPtr<T>` that share one control block holding two counters:

- the **strong** count (number of `SharedPtr`s): when it reaches 0 the object is deleted;
- the **weak** count (number of `WeakPtr`s): the control block itself is freed only when *both* counts are 0, because a `WeakPtr` still needs it to answer `expired()`.

```cpp
template <class T> class WeakPtr;

template <class T>
class SharedPtr {
public:
    SharedPtr() noexcept;
    explicit SharedPtr(T* p);                    // takes ownership (empty if p is null)
    SharedPtr(const SharedPtr& other) noexcept;
    SharedPtr(SharedPtr&& other) noexcept;
    SharedPtr& operator=(const SharedPtr& other) noexcept;
    SharedPtr& operator=(SharedPtr&& other) noexcept;
    ~SharedPtr();

    void reset() noexcept;                       // drop ownership
    T* get() const noexcept;
    long use_count() const noexcept;             // strong count, 0 if empty
    T& operator*() const;
    T* operator->() const noexcept;
    explicit operator bool() const noexcept;
};

template <class T>
class WeakPtr {
public:
    WeakPtr() noexcept;                          // observes nothing
    WeakPtr(const SharedPtr<T>& s) noexcept;     // observes s's object
    WeakPtr(const WeakPtr& other) noexcept;
    WeakPtr(WeakPtr&& other) noexcept;
    WeakPtr& operator=(const WeakPtr& other) noexcept;
    WeakPtr& operator=(WeakPtr&& other) noexcept;
    ~WeakPtr();

    void reset() noexcept;                       // stop observing
    long use_count() const noexcept;             // current strong count, 0 if expired or empty
    bool expired() const noexcept;               // use_count() == 0
    SharedPtr<T> lock() const noexcept;          // a new owner, or an empty SharedPtr if expired
};
```

## Examples

**Example 1**
```cpp
WeakPtr<Session> w;
{
    SharedPtr<Session> s(new Session{1});
    w = WeakPtr<Session>(s);
    w.expired();          // false
    w.use_count();        // 1 (weak references don't count)
    SharedPtr<Session> t = w.lock();
    t->id;                // 1
    s.use_count();        // 2
}                         // last SharedPtr gone: the Session is deleted here
w.expired();              // true
bool(w.lock());           // false
```

**Example 2**
```cpp
SharedPtr<Session> s(new Session{2});
WeakPtr<Session> w(s);
s.reset();                // Session deleted now, even though w still exists
w.expired();              // true; w keeps only the control block alive
w.reset();                // now the control block is freed too
```

## Constraints

- The object is destroyed exactly when the strong count reaches 0, never earlier or later, regardless of weak references.
- The control block is freed exactly when the last `SharedPtr` *and* the last `WeakPtr` are gone (no leaks, no use-after-free).
- Counts are updated atomically. `lock()` must never resurrect an object whose strong count already reached 0, even if another thread is dropping the last `SharedPtr` at the same moment.
- Self-assignment must be safe. All operations are O(1).
