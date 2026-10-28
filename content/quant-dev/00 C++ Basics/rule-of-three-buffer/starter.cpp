#include <cstddef>
#include <cstring>
#include <iostream>
#include <string>

class Buffer {
public:
    explicit Buffer(const char* s) : data_(nullptr), size_(0) {
        // TODO: allocate and copy s
    }
    // TODO: copy constructor, copy assignment operator, destructor (the rule of three)
    void setChar(std::size_t i, char c) { /* TODO */ }
    void append(const char* s) { /* TODO */ }
    const char* c_str() const { return data_ ? data_ : ""; }
    std::size_t size() const { return size_; }

private:
    char* data_;
    std::size_t size_;
};

int main() {
    std::string s, t;
    std::cin >> s >> t;
    Buffer a(s.c_str());
    // TODO: the sequence from the problem statement, then print a, b and c
    return 0;
}
