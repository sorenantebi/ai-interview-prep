---
topic: "C++ Basics"
difficulty: Medium
---
# Rule of Three: A Deep-Copying String Buffer

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`) with a class `Buffer` that **owns** a heap-allocated, null-terminated `char` array:

```cpp
class Buffer {
public:
    explicit Buffer(const char* s);            // allocate strlen(s) + 1 chars and copy
    Buffer(const Buffer& other);               // deep copy
    Buffer& operator=(const Buffer& other);    // deep copy; must survive self-assignment
    ~Buffer();                                 // delete[]
    void setChar(std::size_t i, char c);       // overwrite one character
    void append(const char* s);                // grow: new array, copy both parts, free the old one
    const char* c_str() const;
    std::size_t size() const;
private:
    char* data_;
    std::size_t size_;
};
```

`main` reads two words `s` and `t` and runs exactly:

```cpp
Buffer a(s);
Buffer b = a;          // copy constructor
Buffer c("x");
c = a;                 // copy assignment
a = a;                 // self-assignment must leave a intact
b.setChar(0, '#');
c.append(t);
```

then prints three lines `a = <a> (<size>)`, `b = ...`, `c = ...`. If your copies were shallow (the compiler-generated ones just copy the pointer), `a` would change too and the program would free the same memory twice.

## Examples

**Example 1**
```text
Input:
hello world
Output:
a = hello (5)
b = #ello (5)
c = helloworld (10)
```

**Example 2**
```text
Input:
a b
Output:
a = a (1)
b = # (1)
c = ab (2)
```

## Constraints

- Each word has `1..100` characters.
- No `std::string` inside `Buffer`; manage the memory with `new[]` / `delete[]`. `<cstring>` functions (`std::strlen`, `std::memcpy`) are allowed.
