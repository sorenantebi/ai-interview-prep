---
topic: "Templates & Compile Time"
difficulty: Hard
---
# Type-Erased Function Wrapper

**Topic:** Templates & Compile Time · **Difficulty:** Hard

## Problem

Event-driven trading systems register callbacks everywhere: "on fill", "on timer", "on market data". The callbacks are lambdas with different captures, plain functions and functor objects, all different types, yet they must sit in one container. `std::function` solves this with **type erasure**: a fixed outer type that hides the concrete callable behind an internal interface. Interviewers ask you to build it to see whether you understand templates, virtual dispatch, ownership and copying together.

Implement `Function<R(Args...)>`:

```cpp
template <class Signature> class Function;     // primary template: left undefined

template <class R, class... Args>
class Function<R(Args...)> {
public:
    Function() noexcept;                       // empty
    Function(std::nullptr_t) noexcept;         // empty
    template <class F> Function(F f);          // any callable invocable as R(Args...)
    Function(const Function& other);           // deep copy: the copy has its own captured state
    Function(Function&& other) noexcept;       // other becomes empty
    Function& operator=(const Function& other);
    Function& operator=(Function&& other) noexcept;
    ~Function();

    R operator()(Args... args) const;          // throws std::bad_function_call if empty
    explicit operator bool() const noexcept;   // true if it holds a callable
};
```

Make sure the template constructor doesn't hijack copying: `Function g = f;` with a non-const `f` must call the copy constructor, not wrap a `Function` inside a `Function`.

## Examples

**Example 1**
```cpp
Function<int(int, int)> add = [](int a, int b) { return a + b; };
add(2, 3);                                // 5

int (*fp)(int, int) = [](int a, int b) { return a * b; };
Function<int(int, int)> mul = fp;
mul(4, 5);                                // 20
```

**Example 2**
```cpp
Function<int()> counter = [n = 0]() mutable { return ++n; };
counter();                                // 1
Function<int()> copy = counter;           // copies the captured n (== 1)
counter();                                // 2
copy();                                   // 2  (independent state)

Function<void()> empty;
bool(empty);                              // false
empty();                                  // throws std::bad_function_call
```

## Constraints

- No `std::function`, `std::any` or `std::move_only_function`.
- No leaks: every captured object that is created is destroyed exactly once (a test counts them).
- Calls must forward arguments without extra copies of reference parameters (e.g. `Function<void(int&)>` can modify the caller's variable).
