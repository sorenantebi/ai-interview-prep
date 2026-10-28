---
topic: "C++ Basics"
difficulty: Easy
---
# Bit Manipulation on a 16-Bit Register - Solution

## Intuition

A mask with only bit `k` set is `1u << k`. OR-ing it in sets the bit, AND-ing with its complement clears it, XOR flips it, and AND-ing tests it. Two classic tricks: `x & (x - 1)` removes the lowest set bit, so counting how many times you can do that before reaching 0 counts the ones (Kernighan), and a non-zero `x` is a power of two exactly when `x & (x - 1) == 0`.

## Approach

1. `set`: `x |= 1u << k`; `clear`: `x &= ~(1u << k)`; `toggle`: `x ^= 1u << k`; `test`: `(x >> k) & 1u`.
2. `count`: `for (v = x; v; v &= v - 1) ++c;`
3. `pow2`: `x != 0 && (x & (x - 1)) == 0`.
4. `print`: for `k` from 15 down to 0 print `(x >> k) & 1`.

Note: in `x |= 1u << k` the operands are promoted to `unsigned int` and the result is narrowed back to 16 bits on assignment; `~(1u << k)` has 32 bits, but the upper ones are cut off harmlessly by the `&=`.

## Code

```cpp
#include <cstdint>
#include <iostream>
#include <string>

int main() {
    unsigned initial;
    int q;
    std::cin >> initial >> q;
    std::uint16_t x = static_cast<std::uint16_t>(initial);
    while (q--) {
        std::string cmd;
        std::cin >> cmd;
        if (cmd == "set" || cmd == "clear" || cmd == "toggle" || cmd == "test") {
            int k;
            std::cin >> k;
            unsigned mask = 1u << k;
            if (cmd == "set") x |= mask;
            else if (cmd == "clear") x &= ~mask;
            else if (cmd == "toggle") x ^= mask;
            else std::cout << ((x >> k) & 1u) << '\n';
        } else if (cmd == "count") {
            int c = 0;
            for (unsigned v = x; v; v &= v - 1) ++c;
            std::cout << c << '\n';
        } else if (cmd == "pow2") {
            std::cout << (x != 0 && (x & (x - 1)) == 0 ? "yes" : "no") << '\n';
        } else if (cmd == "print") {
            for (int k = 15; k >= 0; --k) std::cout << ((x >> k) & 1u);
            std::cout << ' ' << x << '\n';
        }
    }
    return 0;
}
```

## Complexity

- Time: O(1) per command (at most 16 steps).
- Space: O(1)

## Interview follow-ups

- Why use `1u << k` rather than `1 << k`? What is `1 << 31` on a 32-bit `int`, and `1 << 32`? (Shifting into the sign bit was UB before C++20; shifting by >= the width is always UB.)
- How do you isolate the lowest set bit? (`x & -x`.) Swap two values with XOR? Check if `x` is even?
- What does right-shifting a negative signed integer do? (Arithmetic shift, guaranteed since C++20.)
- What are `std::popcount`, `std::countr_zero` and `std::bit_width` (C++20 `<bit>`), and what instructions do they compile to?
- Where do bit tricks show up in trading systems? (Packing flags into a message field, order-book bitmaps of occupied price levels, fast modulo by a power of two with `& (n - 1)` in ring buffers.)
