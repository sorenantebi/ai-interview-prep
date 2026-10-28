---
topic: "Smart Pointers & RAII"
difficulty: Medium
---
# Implement a String Class

**Topic:** Smart Pointers & RAII · **Difficulty:** Medium

## Problem

"Write your own string" is the classic test of the rule of five. A class that owns a heap buffer has to get every special member right: copies must be deep, moves must steal the buffer without allocating (moves happen constantly when strings sit in containers on a hot path), assignment must survive `s = s`, and nothing may leak or be freed twice.

Implement `String`, which owns a NUL-terminated `char` buffer:

```cpp
class String {
public:
    String();                                   // empty string ""
    String(const char* s);                      // copies s (s is never null); implicit on purpose
    String(const String& other);                // deep copy
    String(String&& other) noexcept;            // steals the buffer; other becomes "" (no allocation)
    String& operator=(const String& other);     // deep copy, self-assignment safe
    String& operator=(String&& other) noexcept; // steals the buffer, self-assignment safe
    ~String();

    std::size_t size() const noexcept;          // number of chars, excluding the terminator
    const char* c_str() const noexcept;         // never null, always NUL-terminated
    String& operator+=(const String& other);    // append; s += s must work

    friend bool operator==(const String& a, const String& b) noexcept;  // same characters
};
```

A single `String& operator=(String other)` (copy-and-swap) is an acceptable replacement for the two assignment operators. Strings never contain an embedded `'\0'`.

## Examples

**Example 1**
```cpp
String a("BUY");
String b = a;           // deep copy
b += " 100 AAPL";
a.c_str();              // "BUY"
b.c_str();              // "BUY 100 AAPL"
b.size();               // 12
a == String("BUY");     // true
```

**Example 2**
```cpp
String s("ab");
s += s;                 // "abab"
String t = std::move(s);
t.c_str();              // "abab"
s.size();               // 0
s.c_str();              // "": a moved-from String is still valid
s = t;
s == t;                 // true
```

## Constraints

- No leaks and no double frees (the tests count heap allocations).
- Moving a `String` (construction or assignment) performs no heap allocation.
- `operator+=` runs in amortized O(length of the appended text): grow the buffer geometrically instead of reallocating on every append.
