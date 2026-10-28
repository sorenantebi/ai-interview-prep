---
topic: "C++ Basics"
difficulty: Easy
---
# Swap Three Ways - Solution

## Intuition

C++ passes arguments by value unless told otherwise. `swapByValue` swaps its own private copies, which vanish when it returns, so the caller sees nothing. A pointer is also passed by value, but the copy holds the same address, so writing through `*x` changes the caller's variable. A reference is another name for the caller's variable itself, so assigning to it changes the original directly.

## Approach

1. Read `a` and `b`.
2. For each function: make fresh copies `x = a, y = b`, call the function (`swapByPointer(&x, &y)` needs the addresses), print `x y`.
3. All three bodies are the same three-line swap; only the parameter types differ.

## Code

```cpp
#include <iostream>

void swapByValue(int x, int y) {
    int tmp = x;
    x = y;
    y = tmp;
}

void swapByPointer(int* x, int* y) {
    int tmp = *x;
    *x = *y;
    *y = tmp;
}

void swapByReference(int& x, int& y) {
    int tmp = x;
    x = y;
    y = tmp;
}

int main() {
    int a, b;
    std::cin >> a >> b;

    int x = a, y = b;
    swapByValue(x, y);
    std::cout << "value: " << x << ' ' << y << '\n';

    x = a, y = b;
    swapByPointer(&x, &y);
    std::cout << "pointer: " << x << ' ' << y << '\n';

    x = a, y = b;
    swapByReference(x, y);
    std::cout << "reference: " << x << ' ' << y << '\n';
    return 0;
}
```

## Complexity

- Time: O(1)
- Space: O(1)

## Interview follow-ups

- What can a pointer do that a reference can't? (Be null, be reseated to point elsewhere, do arithmetic.) And vice versa? (A reference must be bound at initialisation and can't be null.)
- Can you swap two ints without a temporary? (XOR swap or `x = x + y` tricks; why they break when `x` and `y` alias the same object, and why nobody does it in production.)
- Why does `const T&` exist for parameters you don't modify? (Avoids a copy of a large object while promising not to change it; can bind to temporaries.)
- How would you write `swap` once for every type? (`template <typename T> void swap(T&, T&)`, ideally using `std::move`.)
