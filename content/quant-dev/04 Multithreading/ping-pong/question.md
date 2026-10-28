---
topic: "Multithreading"
difficulty: Easy
---
# Ping-Pong Threads

**Topic:** Multithreading · **Difficulty:** Easy

## Problem

A classic warm-up in HFT phone screens: make two threads take strict turns. It tests whether you can hand control from one thread to another without busy-waiting forever, missing a wake-up or deadlocking at the end, which is exactly the hand-off logic inside every queue and pipeline stage.

Write a function that starts **two threads**: one appends `"ping"`, the other appends `"pong"`, to a shared sequence. They must strictly alternate, starting with `"ping"`, and each thread appends its word exactly `n` times. Return the sequence joined with single spaces.

```cpp
std::string play(int n);
```

Use a mutex plus a condition variable (or atomics). Both threads must be joined before `play` returns.

## Examples

**Example 1**
```cpp
play(1);   // "ping pong"
```

**Example 2**
```cpp
play(3);   // "ping pong ping pong ping pong"
```

**Example 3**
```cpp
play(0);   // "" (no words, both threads still start and finish)
```

## Constraints

- `0 <= n <= 10^5`
- The words must be produced by two different threads, each appending only its own word (the tests cannot check this: honour system).
- No sleeps to force the order; the hand-off must be explicit.
