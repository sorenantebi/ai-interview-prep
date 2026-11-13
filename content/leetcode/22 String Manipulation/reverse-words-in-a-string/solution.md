---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/reverse-words-in-a-string/
---
# Reverse Words in a String - Solution

## Intuition

Splitting on whitespace gives exactly the words, with all extra spaces discarded. Reversing that list and joining with a single space produces the required output.

## Approach

1. Split `s` on runs of whitespace using `s.split()` (no argument), which also drops leading and trailing spaces.
2. Reverse the list of words.
3. Join the words with a single space.

## Code

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        # Remove leading and trailing spaces
        s = s.strip()
        
        # Split the string into words
        words = s.split()
        
        # Reverse the order of words
        words = words[::-1]
        
        # Join the words with a single space
        reversed_str = ' '.join(words)
        
        return reversed_str
```

## Complexity

- **Time:** `O(n)` — splitting, reversing, and joining each touch every character at most once.
- **Space:** `O(n)` — the list of words and the result string.

## Other Approaches

- **Two-pointer scan from the end:** walk backwards over `s`, skip spaces, and collect each word, then join — Time `O(n)` / Space `O(n)`.
- **In-place on a character array (follow-up):** trim and collapse spaces, reverse the whole array, then reverse each word individually — Time `O(n)` / Space `O(1)` extra (only possible with mutable strings, e.g. in C++ or Java char arrays).
