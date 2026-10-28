---
topic: "Smart Pointers & RAII"
difficulty: Medium
---
# Implement a String Class - Solution

## Intuition

The class owns three things: a pointer to a heap buffer, the length, and the capacity. Each special member answers one question about that buffer:

- copy: allocate a new buffer and copy the bytes (two owners must never share one buffer);
- move: take the pointer and leave the source empty, so it costs three word copies and no allocation;
- destructor: free it.

Let the empty string be "no buffer at all" (`data_ == nullptr`) and have `c_str()` return a static `""` in that case. The default constructor and moved-from strings then never allocate.

The trap is `s += s`: if the append reallocates, the source text lives in the buffer about to be freed. So copy from the old buffer into the new one *before* freeing it.

## Approach

1. Members: `char* data_ = nullptr`, `size_t size_ = 0`, `cap_ = 0` (capacity excludes the terminator).
2. `String(const char*)`: `strlen`, allocate `size + 1`, `memcpy` including the terminator.
3. Copy constructor: the same from `other`'s buffer. Copy assignment: copy into a temporary, then `swap` (copy-and-swap). This is self-assignment safe and leaves `*this` untouched if the allocation throws.
4. Move constructor: `std::exchange` each member out of `other`. Move assignment: move into a temporary, then `swap`; on self-move the temporary takes our buffer and the swap hands it straight back.
5. `operator+=`: if it fits, `memcpy` into the spare space. Otherwise allocate `max(2 * cap_, needed)`, copy the old text, copy the appended text (still alive even if it is our own old buffer), terminate, then free the old buffer.
6. `operator==`: equal sizes and `memcmp` of the bytes.

## Code

```cpp
#include <cstddef>
#include <cstring>
#include <utility>

class String {
public:
    String() = default;

    String(const char* s) : size_(std::strlen(s)), cap_(size_) {
        if (size_) {
            data_ = new char[cap_ + 1];
            std::memcpy(data_, s, size_ + 1);
        }
    }

    String(const String& other) : size_(other.size_), cap_(other.size_) {
        if (size_) {
            data_ = new char[cap_ + 1];
            std::memcpy(data_, other.data_, size_ + 1);
        }
    }

    String(String&& other) noexcept
        : data_(std::exchange(other.data_, nullptr)),
          size_(std::exchange(other.size_, 0)),
          cap_(std::exchange(other.cap_, 0)) {}

    String& operator=(const String& other) {
        if (this != &other) String(other).swap(*this);
        return *this;
    }

    String& operator=(String&& other) noexcept {
        String(std::move(other)).swap(*this);
        return *this;
    }

    ~String() { delete[] data_; }

    std::size_t size() const noexcept { return size_; }
    const char* c_str() const noexcept { return data_ ? data_ : ""; }

    String& operator+=(const String& other) {
        const std::size_t n = other.size_;
        if (n == 0) return *this;
        const char* src = other.data_;  // may be our own buffer when other is *this
        if (size_ + n > cap_) {
            std::size_t new_cap = cap_ * 2 > size_ + n ? cap_ * 2 : size_ + n;
            char* buf = new char[new_cap + 1];
            if (size_) std::memcpy(buf, data_, size_);
            std::memcpy(buf + size_, src, n);  // copy before the old buffer is freed
            delete[] data_;
            data_ = buf;
            cap_ = new_cap;
        } else {
            std::memcpy(data_ + size_, src, n);  // no overlap: src ends where we start writing
        }
        size_ += n;
        data_[size_] = '\0';
        return *this;
    }

    friend bool operator==(const String& a, const String& b) noexcept {
        return a.size_ == b.size_ && std::memcmp(a.c_str(), b.c_str(), a.size_) == 0;
    }

    void swap(String& other) noexcept {
        std::swap(data_, other.data_);
        std::swap(size_, other.size_);
        std::swap(cap_, other.cap_);
    }

private:
    char* data_ = nullptr;
    std::size_t size_ = 0;
    std::size_t cap_ = 0;
};
```

## Complexity

- Time: copy O(n); move O(1); `+=` amortized O(appended length) thanks to doubling; `==` O(n).
- Space: O(capacity), at most about twice the length after appends.

## Interview follow-ups

- Small string optimization: store short strings (say up to 15 chars) inside the object itself. What does that change for move (it is no longer free) and for `sizeof(String)`?
- Why is copy-and-swap exception safe, and what does it cost compared to reusing the existing buffer when it is big enough?
- Add `operator+(const String&, const String&)`. How do you avoid an extra copy for `a + b + c`?
- Why should the move constructor be `noexcept`? What does `std::vector<String>` do on reallocation if it isn't?
- Copy-on-write strings were once common (pre-C++11 libstdc++). Why does the C++11 standard effectively forbid them?
