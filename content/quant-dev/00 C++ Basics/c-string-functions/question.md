---
topic: "C++ Basics"
difficulty: Easy
---
# Write Your Own C-String Functions

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`). Implement these functions on null-terminated `char` arrays, walking pointers until the terminating `'\0'`:

```cpp
std::size_t my_strlen(const char* s);            // number of chars before '\0'
char* my_strcpy(char* dst, const char* src);     // copies src including '\0', returns dst
char* my_strcat(char* dst, const char* src);     // appends src at the end of dst, returns dst
int my_strcmp(const char* a, const char* b);     // <0, 0 or >0, comparing as unsigned char
```

The program reads `q`, then `q` lines each holding two words `a` and `b` (no spaces inside a word). Read each word into a `char` array. For each line print

```text
<len a> <len b> <cmp> <a+b>
```

where `<cmp>` is `-1`, `0` or `1` (the **sign** of `my_strcmp(a, b)`) and `<a+b>` is the concatenation, built in a separate `char` buffer with `my_strcpy` followed by `my_strcat`.

## Examples

**Example 1**
```text
Input:
2
cat dog
apple apple
Output:
3 3 -1 catdog
5 5 0 appleapple
```

**Example 2**
```text
Input:
1
zebra ant
Output:
5 3 1 zebraant
```

## Constraints

- `1 <= q <= 100`, each word has `1..100` characters.
- Don't use `<cstring>` / `std::string` for the work (reading input into a `char` array is fine).
