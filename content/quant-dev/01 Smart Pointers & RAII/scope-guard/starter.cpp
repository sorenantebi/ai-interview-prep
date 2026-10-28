#include <utility>

template <class F>
class ScopeGuard {
public:
    explicit ScopeGuard(F f) {}
    ScopeGuard(ScopeGuard&& other) noexcept {}
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    ScopeGuard& operator=(ScopeGuard&&) = delete;
    ~ScopeGuard() {}
    void dismiss() noexcept {}
};

template <class F>
ScopeGuard<F> make_scope_guard(F f) {
    return ScopeGuard<F>(std::move(f));
}
