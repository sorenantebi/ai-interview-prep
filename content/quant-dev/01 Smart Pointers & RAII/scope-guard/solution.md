---
topic: "Smart Pointers & RAII"
difficulty: Easy
---
# Implement a ScopeGuard - Solution

## Intuition

Destructors run on every way out of a scope: normal fall-through, `return`, `break`, and exception unwinding. So the guard just stores the callable and an `active_` flag, and the destructor calls the callable if the flag is still set. `dismiss()` clears the flag. A move copies the callable and clears the *source's* flag, so exactly one guard is responsible at any time.

## Approach

1. Members: `F f_` and `bool active_ = true`.
2. Destructor: `if (active_) f_();`.
3. `dismiss()`: `active_ = false`.
4. Move constructor: move `f_` from `other`, copy its `active_`, then `other.dismiss()`.
5. Delete copying (two guards would run the cleanup twice) and move assignment (replacing a live guard would have to decide whether to run the old action, which is surprising).
6. `make_scope_guard` just returns `ScopeGuard<F>(std::move(f))`; with C++17 guaranteed copy elision no move happens.

## Code

```cpp
#include <utility>

template <class F>
class ScopeGuard {
public:
    explicit ScopeGuard(F f) : f_(std::move(f)) {}

    ScopeGuard(ScopeGuard&& other) noexcept : f_(std::move(other.f_)), active_(other.active_) {
        other.dismiss();
    }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    ScopeGuard& operator=(ScopeGuard&&) = delete;

    ~ScopeGuard() {
        if (active_) f_();
    }

    void dismiss() noexcept { active_ = false; }

private:
    F f_;
    bool active_ = true;
};

template <class F>
ScopeGuard<F> make_scope_guard(F f) {
    return ScopeGuard<F>(std::move(f));
}
```

## Complexity

- Time: O(1) to create, dismiss or run (plus whatever the callable does).
- Space: the size of the callable plus one `bool`; no heap allocation for lambdas.

## Interview follow-ups

- What happens if the callable throws during stack unwinding? (Two active exceptions: `std::terminate`.) How would you defend against it?
- Implement `SCOPE_EXIT { ... };` as a macro, and `SCOPE_FAIL` / `SCOPE_SUCCESS` variants using `std::uncaught_exceptions()`.
- Why is a scope guard better than storing a `std::function` (allocation, indirect call)?
- Should the move constructor be `noexcept` if `F`'s move can throw? What does that imply for `std::vector<ScopeGuard<F>>`?
