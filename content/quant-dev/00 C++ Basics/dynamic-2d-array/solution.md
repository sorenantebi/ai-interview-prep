---
topic: "C++ Basics"
difficulty: Medium
---
# Transpose a Dynamic 2-D Array - Solution

## Intuition

An `int**` is a pointer to the first of `rows` pointers, each of which points to a separate block of `cols` ints. `m[i][j]` first follows `m[i]` to the row, then indexes into it. The transpose just swaps the roles: `t[j][i] = m[i][j]`. Every `new[]` needs exactly one matching `delete[]`, and the rows must be freed before the array holding their addresses.

## Approach

1. `allocMatrix`: `int** m = new int*[rows]; for each i: m[i] = new int[cols];`
2. Read into `m`, allocate `t = allocMatrix(c, r)`, fill `t[j][i] = m[i][j]`.
3. Print `t`, then `freeMatrix(m, r)` and `freeMatrix(t, c)` (note the row counts differ).

## Code

```cpp
#include <iostream>

int** allocMatrix(int rows, int cols) {
    int** m = new int*[rows];
    for (int i = 0; i < rows; ++i) m[i] = new int[cols];
    return m;
}

void freeMatrix(int** m, int rows) {
    for (int i = 0; i < rows; ++i) delete[] m[i];
    delete[] m;
}

int main() {
    int r, c;
    std::cin >> r >> c;
    int** m = allocMatrix(r, c);
    for (int i = 0; i < r; ++i)
        for (int j = 0; j < c; ++j) std::cin >> m[i][j];

    int** t = allocMatrix(c, r);
    for (int i = 0; i < r; ++i)
        for (int j = 0; j < c; ++j) t[j][i] = m[i][j];

    for (int j = 0; j < c; ++j)
        for (int i = 0; i < r; ++i) std::cout << t[j][i] << (i + 1 < r ? ' ' : '\n');

    freeMatrix(m, r);
    freeMatrix(t, c);
    return 0;
}
```

## Complexity

- Time: O(r * c)
- Space: O(r * c) for each matrix, plus `r` (or `c`) row pointers.

## Interview follow-ups

- What's wrong with `delete[] m` alone? With freeing the rows after `delete[] m`? (Leak; use-after-free.)
- Why is one contiguous `new int[r * c]` indexed as `a[i * c + j]` usually faster? (One allocation, cache-friendly, no pointer chasing.) How would you wrap it in a class?
- If the 3rd `new int[cols]` throws `std::bad_alloc`, what leaks, and how do RAII types (`std::vector`, `std::unique_ptr<int[]>`) fix that?
- How do you transpose a square matrix in place? Why is a naive transpose of a large matrix cache-unfriendly, and what does blocking/tiling buy you?
