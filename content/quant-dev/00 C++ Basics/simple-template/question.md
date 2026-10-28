---
topic: "C++ Basics"
difficulty: Medium
---
# A Fixed-Capacity Template Stack

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`) with two function templates and a class template:

```cpp
template <typename T> const T& maxOf(const T& a, const T& b);   // the larger (a if equal)
template <typename T> void swapValues(T& a, T& b);               // by hand, with a temporary

template <typename T, int Capacity>
class Stack {                    // storage is a plain array member:  T data_[Capacity];
public:
    bool push(const T& value);   // false if full
    bool pop();                  // false if empty
    T& top();                    // precondition: not empty
    int size() const;
    bool empty() const;
    // ... whatever else you need, e.g. access to the element below the top
};
```

The first input line is `int` or `string`; use a `Stack<int, 4>` or a `Stack<std::string, 4>` accordingly (write the command loop once, as a function template). Then commands follow until end of input:

- `push x` - push `x`, or print `full` if the stack already holds 4 items
- `pop` - print the top value and remove it, or print `empty`
- `max` - print `maxOf` the top two items (without removing them), or `need 2`
- `swap` - swap the top two items with `swapValues` (print nothing), or print `need 2`
- `size` - print the number of items

## Examples

**Example 1**
```text
Input:
int
push 3
push 7
max
swap
pop
size
Output:
7
3
1
```

**Example 2**
```text
Input:
string
pop
push beta
push alpha
max
Output:
empty
beta
```

## Constraints

- At most `1000` commands; integers fit in `int`, strings have no spaces.
- No `std::stack`, `std::vector`, `std::max` or `std::swap`.
