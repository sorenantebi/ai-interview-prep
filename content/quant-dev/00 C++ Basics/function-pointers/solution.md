---
topic: "C++ Basics"
difficulty: Easy
---
# Calculator With a Table of Function Pointers - Solution

## Intuition

A function's name decays to a pointer to it, just like an array's name decays to a pointer to its first element. A pointer of type `long long (*)(long long, long long)` can hold any function with that exact signature, and calling through it (`op(a, b)`) runs whichever one it points to. A table of such pointers turns "which operation?" into data, the idea behind dispatch tables and message handlers indexed by message type.

## Approach

1. Write the six functions with the same signature.
2. `const char symbols[] = {'+', '-', '*', '/', '%', '^'};` and `const BinaryOp ops[] = {add, sub, mul, divide, mod, power};`.
3. `lookup` scans `symbols` and returns `ops[i]` on a match, else `nullptr`.
4. In `main`: unknown check, then the zero-divisor check (`op == divide || op == mod`, comparing function pointers), then print `op(a, b)`.

## Code

```cpp
#include <iostream>

using BinaryOp = long long (*)(long long, long long);

long long add(long long a, long long b) { return a + b; }
long long sub(long long a, long long b) { return a - b; }
long long mul(long long a, long long b) { return a * b; }
long long divide(long long a, long long b) { return a / b; }
long long mod(long long a, long long b) { return a % b; }
long long power(long long a, long long b) {
    long long r = 1;
    while (b-- > 0) r *= a;
    return r;
}

const char symbols[] = {'+', '-', '*', '/', '%', '^'};
const BinaryOp ops[] = {add, sub, mul, divide, mod, power};
const int numOps = sizeof(ops) / sizeof(ops[0]);

BinaryOp lookup(char symbol) {
    for (int i = 0; i < numOps; ++i)
        if (symbols[i] == symbol) return ops[i];
    return nullptr;
}

int main() {
    int q;
    std::cin >> q;
    while (q--) {
        long long a, b;
        char symbol;
        std::cin >> a >> symbol >> b;
        BinaryOp op = lookup(symbol);
        if (!op) std::cout << "unknown\n";
        else if ((op == divide || op == mod) && b == 0) std::cout << "error\n";
        else std::cout << op(a, b) << '\n';
    }
    return 0;
}
```

## Complexity

- Time: O(1) per expression (six table entries), plus O(b) for `^`.
- Space: O(1)

## Interview follow-ups

- Read these declarations aloud: `int (*f)(int)`, `int* f(int)`, `int (*arr[4])(int)`, `int (*(*g)(char))(int)`. Why do people use `using` aliases?
- Function pointer vs `std::function` vs a template parameter (lambda): which can be inlined, which allocates, which can hold captured state?
- What is a pointer to member function (`long long (Calc::*)(long long)`) and how do you call it?
- Make `lookup` O(1): index a 256-entry table by `(unsigned char)symbol`.
- What do `-7 / 2` and `-7 % 2` give in C++? (`-3` and `-1`: truncation towards zero.)
