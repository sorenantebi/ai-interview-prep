#include <utility>

template <class Closer>
class Handle {
public:
    Handle(int id, Closer closer) : closer_(closer) {}
    ~Handle() {}

    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;
    Handle(Handle&& other) noexcept : closer_(other.closer_) {}
    Handle& operator=(Handle&& other) noexcept { return *this; }

    int get() const noexcept { return -1; }
    bool valid() const noexcept { return false; }
    int release() noexcept { return -1; }
    void reset(int id = -1) {}

private:
    Closer closer_;
};
