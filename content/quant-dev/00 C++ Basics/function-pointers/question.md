---
topic: "C++ Basics"
difficulty: Easy
---
# Calculator With a Table of Function Pointers

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`) that evaluates simple integer expressions by **looking up a function pointer** instead of using a `switch` or `if` chain on the operator.

```cpp
using BinaryOp = long long (*)(long long, long long);

long long add(long long a, long long b);
long long sub(long long a, long long b);
long long mul(long long a, long long b);
long long divide(long long a, long long b);   // truncates towards zero, like C++ '/'
long long mod(long long a, long long b);      // like C++ '%'
long long power(long long a, long long b);    // a^b for b >= 0, by repeated multiplication

BinaryOp lookup(char symbol);                 // + - * / % ^  -> the function; anything else -> nullptr
```

Store the six operators in two parallel arrays (`const char symbols[]` and `const BinaryOp ops[]`) and make `lookup` search them. The program reads `q`, then `q` lines `a op b` and prints one line per expression:

- `unknown` if `lookup` returns `nullptr`,
- `error` if the operator is `/` or `%` and `b == 0`,
- otherwise the result of calling the function **through the pointer**.

## Examples

**Example 1**
```text
Input:
4
3 + 4
10 / 3
7 % 0
2 ^ 10
Output:
7
3
error
1024
```

**Example 2**
```text
Input:
2
5 ? 1
-6 * 7
Output:
unknown
-42
```

## Constraints

- `1 <= q <= 1000`, `|a|, |b| <= 10^6`; for `^`, `0 <= b` and the result fits in `long long`.
- The operator is a single non-space character.
