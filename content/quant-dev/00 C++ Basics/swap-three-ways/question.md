---
topic: "C++ Basics"
difficulty: Easy
---
# Swap Three Ways

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`). It reads two integers `a` and `b` from standard input. Implement three swap functions that differ only in how they receive their arguments:

```cpp
void swapByValue(int x, int y);         // receives copies
void swapByPointer(int* x, int* y);     // receives addresses
void swapByReference(int& x, int& y);   // receives aliases
```

Each function body swaps its two parameters with a temporary (no `std::swap`). In `main`, for each function **start again from the original `a` and `b`**, call the function on copies of them, and print what the caller sees afterwards:

```text
value: <x> <y>
pointer: <x> <y>
reference: <x> <y>
```

The output shows which calling conventions actually change the caller's variables.

## Examples

**Example 1**
```text
Input:
3 7
Output:
value: 3 7
pointer: 7 3
reference: 7 3
```

**Example 2**
```text
Input:
-5 5
Output:
value: -5 5
pointer: 5 -5
reference: 5 -5
```

## Constraints

- `-10^9 <= a, b <= 10^9`
- Write the swap by hand with a temporary; don't use `std::swap`.
