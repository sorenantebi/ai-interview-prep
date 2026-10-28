---
topic: "C++ Basics"
difficulty: Medium
---
# A Fixed-Capacity Template Stack - Solution

## Intuition

A template is a recipe the compiler instantiates once per set of template arguments: `Stack<int, 4>` and `Stack<std::string, 4>` are two unrelated classes generated from the same source. A non-type parameter such as `int Capacity` is a compile-time constant, so `T data_[Capacity]` is an ordinary fixed-size array inside the object, with no heap allocation. The function templates only require that `T` supports `<` (for `maxOf`) and copying (for `swapValues`); `int` and `std::string` both do.

## Approach

1. `maxOf`: `return a < b ? b : a;` (returns `a` on ties). `swapValues`: `T tmp = a; a = b; b = tmp;`.
2. `Stack`: `size_` counts items; `push` writes `data_[size_++]`; `pop` decrements; `top()` is `data_[size_ - 1]`; `below()` is `data_[size_ - 2]`.
3. `run<T>()` reads commands; `push` reads a `T` with `>>`, which works for both types.

## Code

```cpp
#include <iostream>
#include <string>

template <typename T>
const T& maxOf(const T& a, const T& b) { return a < b ? b : a; }

template <typename T>
void swapValues(T& a, T& b) {
    T tmp = a;
    a = b;
    b = tmp;
}

template <typename T, int Capacity>
class Stack {
public:
    bool push(const T& value) {
        if (size_ == Capacity) return false;
        data_[size_++] = value;
        return true;
    }
    bool pop() {
        if (size_ == 0) return false;
        --size_;
        return true;
    }
    T& top() { return data_[size_ - 1]; }
    T& below() { return data_[size_ - 2]; }
    int size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    T data_[Capacity];
    int size_ = 0;
};

template <typename T>
void run() {
    Stack<T, 4> s;
    std::string cmd;
    while (std::cin >> cmd) {
        if (cmd == "push") {
            T value;
            std::cin >> value;
            if (!s.push(value)) std::cout << "full\n";
        } else if (cmd == "pop") {
            if (s.empty()) std::cout << "empty\n";
            else { std::cout << s.top() << '\n'; s.pop(); }
        } else if (cmd == "max" || cmd == "swap") {
            if (s.size() < 2) std::cout << "need 2\n";
            else if (cmd == "max") std::cout << maxOf(s.top(), s.below()) << '\n';
            else swapValues(s.top(), s.below());
        } else if (cmd == "size") {
            std::cout << s.size() << '\n';
        }
    }
}

int main() {
    std::string type;
    std::cin >> type;
    if (type == "int") run<int>();
    else run<std::string>();
    return 0;
}
```

## Complexity

- Time: O(1) per command (string copies aside).
- Space: O(Capacity), inside the `Stack` object itself.

## Interview follow-ups

- Why do templates usually live entirely in header files? (The compiler needs the definition to instantiate it in each translation unit.)
- What error do you get calling `maxOf(3, 4.5)`, and how do you fix it? (Deduction conflict: `maxOf<double>(3, 4.5)`.)
- Why does `maxOf` returning `const T&` dangle in `const int& m = maxOf(1, 2);`?
- `T data_[Capacity]` default-constructs all `Capacity` elements up front. How do real containers avoid that? (Raw aligned storage plus placement `new`, `std::optional`, or `std::array` for trivial types.)
- How would you restrict `T` to types with `<`? (C++20 concepts: `template <std::totally_ordered T>`.) What is template specialisation?
