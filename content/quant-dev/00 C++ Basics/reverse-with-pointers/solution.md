---
topic: "C++ Basics"
difficulty: Easy
---
# Reverse an Array With Pointers - Solution

## Intuition

`first` points at the first element and `last` one past the end. Swap `*first` with `*(last - 1)` and walk both pointers inwards until they meet. Pointer arithmetic (`last - 1`, `++first`) moves by whole `int`s, not bytes.

## Approach

1. `int* a = new int[n];` then read into `a[i]` (or `*(a + i)`).
2. `reverse(a, a + n)`: while `first < --last`, swap and `++first`.
3. Print, then `delete[] a;` (not `delete`: memory from `new[]` must be freed with `delete[]`).

## Code

```cpp
#include <iostream>

void reverse(int* first, int* last) {
    while (first < last && first < --last) {
        int tmp = *first;
        *first = *last;
        *last = tmp;
        ++first;
    }
}

int main() {
    int n;
    std::cin >> n;
    int* a = new int[n];
    for (int* p = a; p != a + n; ++p) std::cin >> *p;
    reverse(a, a + n);
    for (int i = 0; i < n; ++i) std::cout << a[i] << (i + 1 < n ? ' ' : '\n');
    delete[] a;
    return 0;
}
```

## Complexity

- Time: O(n)
- Space: O(n) for the array, O(1) extra for the reversal.

## Interview follow-ups

- What happens with `delete a` instead of `delete[] a`? (Undefined behaviour.)
- Why is `last` one past the end (a half-open range), like STL iterators?
- Rewrite `reverse` as a template that works for any type, then for any bidirectional iterator.
