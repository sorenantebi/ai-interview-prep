---
topic: "C++ Basics"
difficulty: Easy
---
# Compile It Yourself

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

The program is written for you: **your job is to build it in two steps**, like a real build does. The first lines of the file are your compile commands, run in order:

```cpp
// compile: g++ main.cpp
```

Replace that line with **two** `// compile:` lines:

1. **Compile** `main.cpp` into an object file called **`main.o`** (no linking yet).
2. **Link** `main.o` into a program called **`trader`**.

The program prints its own file name and whether `main.o` exists, then turns each quantity on stdin into lots of 100.

## Example

Input:
```
250
1000
```

Output:
```
binary trader
object file main.o
250 -> 2 lots
1000 -> 10 lots
```

## Notes

- Don't change the code, only the `// compile:` lines.
- With `g++ main.cpp` both steps happen at once, the object file is thrown away and the program is called `a.out`.
