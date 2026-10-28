---
topic: "C++ Basics"
difficulty: Medium
---
# Transpose a Dynamic 2-D Array

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`). It reads `r` and `c`, then an `r x c` matrix of integers row by row. Store it in a **jagged 2-D array built with `new`**: an array of `r` row pointers, each row its own `new int[c]`. Build its transpose (a `c x r` matrix) the same way, print the transpose row by row (numbers separated by single spaces), and free **every** allocation.

Write and use these helpers:

```cpp
int** allocMatrix(int rows, int cols);      // new int*[rows], then new int[cols] for each row
void freeMatrix(int** m, int rows);         // delete[] each row, then delete[] the row array
```

## Examples

**Example 1**
```text
Input:
2 3
1 2 3
4 5 6
Output:
1 4
2 5
3 6
```

**Example 2**
```text
Input:
1 1
9
Output:
9
```

## Constraints

- `1 <= r, c <= 300`, values fit in `int`.
- No `std::vector`, no fixed-size `int[300][300]`: the point is `new[]` / `delete[]` on pointers to pointers.
