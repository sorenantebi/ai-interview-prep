---
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/valid-palindrome/
neetcode: https://neetcode.io/problems/is-palindrome
---
# Valid Palindrome - Solution

**Question:** Valid Palindrome - Question · **Difficulty:** Easy

## Intuition

Instead of building a cleaned copy, walk two pointers inward from both ends and skip any non-alphanumeric characters on the fly. Compare the lowercase versions of the characters they land on; any mismatch means it is not a palindrome.

## Approach

1. Set `l = 0`, `r = len(s) - 1`.
2. While `l < r`:
   - Advance `l` while `s[l]` is not alphanumeric (and `l < r`).
   - Retreat `r` while `s[r]` is not alphanumeric (and `l < r`).
   - If `s[l].lower() != s[r].lower()`, return `False`.
   - Move both pointers inward.
3. Return `True`.

## Code

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        new = ''
        for a in s:
            if a.isalpha() or a.isdigit():
                new += a.lower()
        return (new == new[::-1])
```

## Complexity

- **Time:** `O(n)` — each pointer crosses the string at most once.
- **Space:** `O(1)` — no filtered copy is built.

## Other Approaches

- **Filter and reverse:** build `t = "".join(c.lower() for c in s if c.isalnum())` and check `t == t[::-1]` — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Two pointers can skip "ignored" elements independently, which avoids allocating a cleaned copy. Note that `_` is not alphanumeric, a classic edge case.
