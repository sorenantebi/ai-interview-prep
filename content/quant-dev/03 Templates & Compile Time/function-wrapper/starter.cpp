#include <cstddef>
#include <functional>  // only for std::bad_function_call
#include <memory>
#include <type_traits>
#include <utility>

template <class Signature>
class Function;

template <class R, class... Args>
class Function<R(Args...)> {
public:
    Function() noexcept {}
    Function(std::nullptr_t) noexcept {}

    template <class F>
        requires(!std::is_same_v<std::decay_t<F>, Function>)
    Function(F f) {}

    Function(const Function& other) {}
    Function(Function&& other) noexcept {}
    Function& operator=(const Function& other) { return *this; }
    Function& operator=(Function&& other) noexcept { return *this; }
    ~Function() {}

    R operator()(Args... args) const { throw std::bad_function_call(); }
    explicit operator bool() const noexcept { return false; }
};
