---
topic: "C++ Basics"
difficulty: Easy
---
# Write Your Own C-String Functions - Solution

## Intuition

A C string is just a pointer to the first `char` of an array that ends with a `'\0'` byte; there's no stored length. So every operation is a pointer walk until that terminator: `strlen` counts steps, `strcpy` copies until (and including) it, `strcat` first walks to `dst`'s terminator and copies from there, and `strcmp` walks both strings while they agree.

## Approach

1. `my_strlen`: `const char* p = s; while (*p) ++p; return p - s;`
2. `my_strcpy`: `while ((*d++ = *src++)) {}` copies the `'\0'` too, then stops.
3. `my_strcat`: `my_strcpy(dst + my_strlen(dst), src)`.
4. `my_strcmp`: advance while `*a && *a == *b`, then return `(unsigned char)*a - (unsigned char)*b`.
5. Buffers: words are at most 100 chars, so `char a[101]`; the concatenation needs `char ab[201]` (200 chars plus `'\0'`).

## Code

```cpp
#include <cstddef>
#include <iostream>

std::size_t my_strlen(const char* s) {
    const char* p = s;
    while (*p) ++p;
    return p - s;
}

char* my_strcpy(char* dst, const char* src) {
    char* d = dst;
    while ((*d++ = *src++)) {}
    return dst;
}

char* my_strcat(char* dst, const char* src) {
    my_strcpy(dst + my_strlen(dst), src);
    return dst;
}

int my_strcmp(const char* a, const char* b) {
    while (*a && *a == *b) ++a, ++b;
    return (unsigned char)*a - (unsigned char)*b;
}

int main() {
    int q;
    std::cin >> q;
    char a[101], b[101], ab[201];
    while (q--) {
        std::cin >> a >> b;  // C++20: reading into a char array is bounded by its size
        int c = my_strcmp(a, b);
        my_strcpy(ab, a);
        my_strcat(ab, b);
        std::cout << my_strlen(a) << ' ' << my_strlen(b) << ' ' << (c > 0) - (c < 0) << ' ' << ab << '\n';
    }
    return 0;
}
```

## Complexity

- Time: O(len a + len b) per line.
- Space: O(1) beyond the fixed buffers.

## Interview follow-ups

- What happens if `dst` is too small for `my_strcpy`? (Buffer overflow, the classic security bug; hence `strncpy`, `strlcpy`, `snprintf`, `std::string`.)
- Why is calling `strlen` in a loop condition (`for (i = 0; i < strlen(s); ++i)`) O(n^2)?
- Why compare as `unsigned char`? (Plain `char` may be signed, so bytes >= 128 would compare as negative.)
- What's the difference between `char s[] = "hi";` and `const char* s = "hi";`? Why can't you modify a string literal?
- What does `sizeof("hello")` return? (6, it includes the `'\0'`.)
