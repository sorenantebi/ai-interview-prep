---
topic: "C++ Basics"
difficulty: Medium
---
# Rule of Three: A Deep-Copying String Buffer - Solution

## Intuition

The compiler-generated copy constructor and assignment copy members one by one, so two `Buffer`s would share one `char*`: writing through one changes the other, and both destructors `delete[]` the same pointer (a double free). The **rule of three**: if a class needs a user-written destructor, it almost certainly needs a user-written copy constructor and copy assignment too. Each copy allocates its own array.

## Approach

1. Constructor: `size_ = strlen(s)`, `data_ = new char[size_ + 1]`, `memcpy` including the `'\0'`.
2. Copy constructor: same thing from `other.data_`.
3. Copy assignment with **copy-and-swap**: take the argument by value (that copy is made by the copy constructor), swap its members with ours, and let its destructor free our old array. That is self-assignment safe and exception safe for free. (The alternative: `if (this != &other)`, allocate the new array **first**, then `delete[]` the old one.)
4. `append`: allocate `size_ + strlen(s) + 1`, copy both parts, `delete[]` the old array, update the members.

## Code

```cpp
#include <cstddef>
#include <cstring>
#include <iostream>
#include <string>
#include <utility>

class Buffer {
public:
    explicit Buffer(const char* s) : data_(nullptr), size_(std::strlen(s)) {
        data_ = new char[size_ + 1];
        std::memcpy(data_, s, size_ + 1);
    }

    Buffer(const Buffer& other) : data_(new char[other.size_ + 1]), size_(other.size_) {
        std::memcpy(data_, other.data_, size_ + 1);
    }

    Buffer& operator=(Buffer other) {  // by value: the copy constructor did the work
        std::swap(data_, other.data_);
        std::swap(size_, other.size_);
        return *this;                   // other's destructor frees our old array
    }

    ~Buffer() { delete[] data_; }

    void setChar(std::size_t i, char c) { data_[i] = c; }

    void append(const char* s) {
        std::size_t extra = std::strlen(s);
        char* grown = new char[size_ + extra + 1];
        std::memcpy(grown, data_, size_);
        std::memcpy(grown + size_, s, extra + 1);
        delete[] data_;
        data_ = grown;
        size_ += extra;
    }

    const char* c_str() const { return data_; }
    std::size_t size() const { return size_; }

private:
    char* data_;
    std::size_t size_;
};

void print(const char* name, const Buffer& buf) {
    std::cout << name << " = " << buf.c_str() << " (" << buf.size() << ")\n";
}

int main() {
    std::string s, t;
    std::cin >> s >> t;
    Buffer a(s.c_str());
    Buffer b = a;
    Buffer c("x");
    c = a;
    a = a;
    b.setChar(0, '#');
    c.append(t.c_str());
    print("a", a);
    print("b", b);
    print("c", c);
    return 0;
}
```

## Complexity

- Time: O(|s| + |t|)
- Space: O(|s| + |t|), three independent arrays.

## Interview follow-ups

- Shallow vs deep copy: what exactly goes wrong with the default copy here? (Aliasing, double `delete[]`, dangling pointer.)
- Implement assignment without copy-and-swap. Why must you allocate before deleting, and why check `this != &other`?
- Rule of five: add a move constructor and move assignment (`noexcept`, steal the pointer, leave the source as `nullptr` / 0). Why does `std::vector<Buffer>` only use your move constructor on reallocation if it's `noexcept`?
- Rule of zero: how would `std::unique_ptr<char[]>` or `std::string` let you delete all five special members?
- Why is the single-argument constructor `explicit`?
