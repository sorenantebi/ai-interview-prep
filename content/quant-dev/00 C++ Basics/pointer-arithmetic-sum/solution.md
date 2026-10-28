---
topic: "C++ Basics"
difficulty: Easy
---
# Sum and Maximum by Walking a Pointer - Solution

## Intuition

`a[i]` is just shorthand for `*(a + i)`. Instead of an index we can hold a pointer `p` and advance it with `++p`, which moves by `sizeof(int)` bytes. Subtracting two pointers into the same array gives the number of elements between them (a `std::ptrdiff_t`), which is exactly the index.

## Approach

1. `sum`: `for (const int* p = first; p != last; ++p) total += *p;` using a `long long` so a large `n` can't overflow.
2. `findMax`: keep `best = first`; for each later `p`, if `*p > *best` (strictly, to keep the first one) set `best = p`.
3. In `main`, print `*m` and `m - a`, then `delete[] a`.

The helpers take `const int*`: they read the array but promise not to change it.

## Code

```cpp
#include <iostream>

long long sum(const int* first, const int* last) {
    long long total = 0;
    for (const int* p = first; p != last; ++p) total += *p;
    return total;
}

const int* findMax(const int* first, const int* last) {
    const int* best = first;
    for (const int* p = first + 1; p < last; ++p)
        if (*p > *best) best = p;
    return best;
}

int main() {
    int n;
    std::cin >> n;
    int* a = new int[n];
    for (int* p = a; p != a + n; ++p) std::cin >> *p;

    std::cout << "sum " << sum(a, a + n) << '\n';
    const int* m = findMax(a, a + n);
    std::cout << "max " << *m << " at " << (m - a) << '\n';

    delete[] a;
    return 0;
}
```

## Complexity

- Time: O(n)
- Space: O(n) for the array, O(1) extra.

## Interview follow-ups

- Is it legal to form the pointer `a + n`? To dereference it? (Forming one-past-the-end is fine; dereferencing it is UB. `a + n + 1` is UB even without dereferencing.)
- What's the difference between `const int* p`, `int* const p` and `const int* const p`?
- Why does `sizeof(a)` give 8 here but `sizeof(arr)` gives `40` for `int arr[10]`? (Array-to-pointer decay.)
- What is the type of `p - q`, and why is subtracting pointers into different arrays undefined?
