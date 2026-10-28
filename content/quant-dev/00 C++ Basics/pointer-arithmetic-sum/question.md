---
topic: "C++ Basics"
difficulty: Easy
---
# Sum and Maximum by Walking a Pointer

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`). It reads `n`, then `n` integers, into an array allocated with `new int[n]`. Implement the two helpers below **by moving a pointer** from `first` to `last` (no `[]` indexing, no index variable inside them):

```cpp
long long sum(const int* first, const int* last);        // sum of [first, last)
const int* findMax(const int* first, const int* last);   // pointer to the first largest element
```

Then print two lines:

```text
sum <total>
max <value> at <index>
```

where `<index>` is the 0-based position of the maximum, computed with **pointer subtraction** (`p - first`). Free the array before exiting.

## Examples

**Example 1**
```text
Input:
5
3 9 2 9 1
Output:
sum 24
max 9 at 1
```

**Example 2**
```text
Input:
1
-7
Output:
sum -7
max -7 at 0
```

## Constraints

- `1 <= n <= 10^5`, `-10^9 <= values <= 10^9`
- If the maximum occurs several times, report its first occurrence.
- No `std::accumulate` / `std::max_element`, no `std::vector`.
