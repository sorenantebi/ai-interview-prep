#include <atomic>
#include <optional>
#include <utility>

template <class T>
class LockFreeStack {
public:
    LockFreeStack() {}
    ~LockFreeStack() {}
    LockFreeStack(const LockFreeStack&) = delete;
    LockFreeStack& operator=(const LockFreeStack&) = delete;

    void push(T value) {}

    std::optional<T> pop() { return std::nullopt; }

    bool empty() const { return true; }
};
