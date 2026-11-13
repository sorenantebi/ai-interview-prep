---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/string-compression/
---
# String Compression - Solution

## Intuition

Compressed output is never longer than the input: a group of length 1 takes 1 cell, and a group of length `k >= 2` takes `1 + len(str(k))` cells, which is at most `k`. So a write pointer can never overtake the read pointer, which allows compressing in place with two pointers.

## Approach

1. Keep a read pointer `read` and a write pointer `write`, both starting at 0.
2. At each step, record the current character and advance `read` while the next characters are equal, to find the group's length.
3. Write the character at `write` and increment `write`.
4. If the group length is greater than 1, write each digit of the length (via `str(count)`) at `write`, advancing `write` for each digit.
5. Repeat until `read` reaches the end of the array.
6. Return `write`, the new length.

## Code

```python
from typing import List, Optional

class Solution:
    def compress(self, chars: List[str]) -> int:
        write = 0
        read = 0
        n = len(chars)
        while read < n:
            ch = chars[read]
            start = read
            while read < n and chars[read] == ch:
                read += 1
            count = read - start
            chars[write] = ch
            write += 1
            if count > 1:
                for d in str(count):
                    chars[write] = d
                    write += 1
        return write
```

## Complexity

- **Time:** `O(n)` — each character is read once and written at most once.
- **Space:** `O(1)` — only pointers and a short digit string (at most 4 digits for `n <= 2000`) are used.

## Other Approaches

- **Build a new list:** Construct the compressed output in a separate list and copy it back into `chars` — Time `O(n)` / Space `O(n)`, which violates the constant-space requirement.
