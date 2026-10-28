---
topic: "Smart Pointers & RAII"
difficulty: Easy
---
# Implement a ScopeGuard

**Topic:** Smart Pointers & RAII · **Difficulty:** Easy

## Problem

Order-entry code often does several steps that must be undone together if a later step fails: reserve risk limits, write a journal entry, register the order with the book. Writing `try/catch` around every step is noisy and easy to get wrong. A scope guard registers a cleanup action that runs automatically when the scope ends, including when an exception unwinds it, and can be *dismissed* once the whole operation has succeeded ("commit").

Implement a class template `ScopeGuard<F>` and a helper `make_scope_guard`:

```cpp
template <class F>
class ScopeGuard {
public:
    explicit ScopeGuard(F f);                  // stores the callable
    ScopeGuard(ScopeGuard&& other) noexcept;   // takes over the duty; other will not run it
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    ScopeGuard& operator=(ScopeGuard&&) = delete;
    ~ScopeGuard();                             // calls f() unless dismissed
    void dismiss() noexcept;                   // cancel: f will not be called
};

template <class F>
ScopeGuard<F> make_scope_guard(F f);
```

Class template argument deduction should let you write `ScopeGuard g([&] { ... });`.

## Examples

**Example 1**
```cpp
int undo = 0;
{
    ScopeGuard g([&] { ++undo; });
}
undo;          // 1: ran at scope exit
{
    auto g = make_scope_guard([&] { ++undo; });
    g.dismiss();
}
undo;          // still 1: dismissed
```

**Example 2**
```cpp
std::vector<std::string> log;
try {
    ScopeGuard g([&] { log.push_back("rollback"); });
    throw std::runtime_error("venue rejected");
} catch (const std::exception&) {}
log;           // {"rollback"}: ran during stack unwinding
```

## Constraints

- The callable runs at most once, even after the guard has been moved.
- The callable is assumed not to throw.
- Guards in the same scope run in reverse order of construction (this falls out of C++ destruction order).
