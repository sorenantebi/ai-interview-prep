---
topic: "Templates & Compile Time"
difficulty: Hard
---
# Type-Erased Function Wrapper - Solution

## Intuition

Split the problem in two. An abstract `Callable` interface knows only the signature: `call(Args...)` and `clone()`. A class template `Model<F>` implements that interface for one concrete callable type `F`. The templated constructor is the only place that knows `F`; it creates a `Model<F>` on the heap and keeps it through a `std::unique_ptr<Callable>`. From then on everything goes through virtual calls, so `Function` itself has one fixed type no matter what it holds. That's type erasure.

## Approach

1. `struct Callable { virtual R call(Args...) = 0; virtual std::unique_ptr<Callable> clone() const = 0; virtual ~Callable() = default; };`
2. `template <class F> struct Model : Callable { F f; ... }`: `call` invokes `f` with `std::forward<Args>(args)...`; `clone` returns `std::make_unique<Model>(f)` (copies the captured state).
3. Template constructor: constrain with `requires(!std::is_same_v<std::decay_t<F>, Function>)` so copying a non-const `Function` picks the copy constructor, then `ptr_ = std::make_unique<Model<F>>(std::move(f))`.
4. Copy constructor: `other.ptr_ ? other.ptr_->clone() : nullptr`. Move: steal the `unique_ptr` (the source becomes empty). Copy assignment: copy-and-swap (`Function tmp(other); std::swap(ptr_, tmp.ptr_);`) which is also self-assignment safe.
5. `operator()`: throw `std::bad_function_call` if empty, otherwise `return ptr_->call(std::forward<Args>(args)...)`. Returning a `void` expression from a `void` function is legal, so `R = void` needs no special case.
6. `unique_ptr` destroys the model, and with it the captured state, exactly once.

## Code

```cpp
#include <cstddef>
#include <functional>  // only for std::bad_function_call
#include <memory>
#include <type_traits>
#include <utility>

template <class Signature>
class Function;

template <class R, class... Args>
class Function<R(Args...)> {
    struct Callable {
        virtual ~Callable() = default;
        virtual R call(Args... args) = 0;
        virtual std::unique_ptr<Callable> clone() const = 0;
    };

    template <class F>
    struct Model final : Callable {
        explicit Model(F fn) : f(std::move(fn)) {}
        R call(Args... args) override { return f(std::forward<Args>(args)...); }
        std::unique_ptr<Callable> clone() const override { return std::make_unique<Model>(f); }
        F f;
    };

public:
    Function() noexcept = default;
    Function(std::nullptr_t) noexcept {}

    template <class F>
        requires(!std::is_same_v<std::decay_t<F>, Function>)
    Function(F f) : ptr_(std::make_unique<Model<F>>(std::move(f))) {}

    Function(const Function& other) : ptr_(other.ptr_ ? other.ptr_->clone() : nullptr) {}
    Function(Function&& other) noexcept = default;

    Function& operator=(const Function& other) {
        Function tmp(other);
        std::swap(ptr_, tmp.ptr_);
        return *this;
    }
    Function& operator=(Function&& other) noexcept = default;
    ~Function() = default;

    R operator()(Args... args) const {
        if (!ptr_) throw std::bad_function_call();
        return ptr_->call(std::forward<Args>(args)...);
    }

    explicit operator bool() const noexcept { return ptr_ != nullptr; }

private:
    std::unique_ptr<Callable> ptr_;
};
```

## Complexity

- Time: one virtual call (plus the callable's own work) per invocation; copying clones the callable with one heap allocation.
- Space: one pointer in `Function`, plus a heap block of size `sizeof(F)` + vptr.

## Interview follow-ups

- Add a **small buffer optimisation**: store callables up to e.g. 32 bytes inline to avoid the heap allocation. What must happen on move now? (You must move-construct into the other buffer; you can't just steal a pointer.)
- Replace the virtual interface with a hand-made table of function pointers (`invoke`, `clone`, `destroy`). Why do some low-latency libraries prefer that?
- Many HFT codebases ban `std::function` on the hot path. Why? (Possible allocation, indirect call, no inlining.) What would you use instead? (Templates / CRTP for static callbacks, a function_ref style non-owning view, or a fixed-size inplace function.)
- How does `std::move_only_function` (C++23) differ, and why can it hold a lambda capturing a `std::unique_ptr`?
- Is calling a `mutable` lambda through a `const operator()` a problem? (`std::function` has the same const hole.)
