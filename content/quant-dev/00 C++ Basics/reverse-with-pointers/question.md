---
topic: "C++ Basics"
difficulty: Easy
---
# Reverse an Array With Pointers

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`). It reads `n`, then `n` integers, from standard input. Store them in an array you allocate with `new int[n]`, reverse the array **in place** using two pointers (`int* left`, `int* right`) and pointer arithmetic, not indices, then print the numbers separated by single spaces on one line and free the memory.

Write a helper with this signature and use it:

```cpp
void reverse(int* first, int* last);  // reverses [first, last)
```

## Examples

**Example 1**
```text
Input:
5
1 2 3 4 5
Output:
5 4 3 2 1
```

**Example 2**
```text
Input:
1
42
Output:
42
```

## Constraints

- `1 <= n <= 10^5`
- No `std::reverse`, no `std::vector`: raw pointers and `new[]` / `delete[]` only (the point of the exercise).
