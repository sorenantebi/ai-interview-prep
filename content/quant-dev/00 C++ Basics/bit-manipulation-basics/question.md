---
topic: "C++ Basics"
difficulty: Easy
---
# Bit Manipulation on a 16-Bit Register

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`) that keeps a `std::uint16_t` "register" and edits it with bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`). It reads the initial decimal value, then `q` commands. Bit `0` is the least significant bit.

- `set k` - set bit `k` to 1
- `clear k` - set bit `k` to 0
- `toggle k` - flip bit `k`
- `test k` - print `1` or `0`
- `count` - print the number of 1 bits
- `pow2` - print `yes` if the value is a power of two, otherwise `no`
- `print` - print all 16 bits, most significant first, then a space and the decimal value

`set`, `clear` and `toggle` print nothing.

## Examples

**Example 1**
```text
Input:
5 6
print
set 1
print
test 2
count
pow2
Output:
0000000000000101 5
0000000000000111 7
1
3
no
```

**Example 2**
```text
Input:
0 4
pow2
toggle 15
print
pow2
Output:
no
1000000000000000 32768
yes
```

## Constraints

- `0 <= initial value <= 65535`, `1 <= q <= 1000`, `0 <= k <= 15`.
- No `std::bitset`, `std::popcount` or `__builtin_popcount`: build each operation from bitwise operators yourself.
