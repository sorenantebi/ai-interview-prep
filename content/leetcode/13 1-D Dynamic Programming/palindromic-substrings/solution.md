---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/palindromic-substrings/
neetcode: https://neetcode.io/problems/palindromic-substrings
---
# Palindromic Substrings - Solution

**Question:** Palindromic Substrings - Question · **Difficulty:** Medium

## Intuition

Every palindrome has a unique center (a character or a gap between two characters). Expanding outward from each of the `2n - 1` centers, every successful expansion step corresponds to exactly one distinct palindromic substring, so we just count them.

## Approach

1. For each `i`, expand around `(i, i)` (odd) and `(i, i + 1)` (even).
2. Each time `s[l] == s[r]` within bounds, increment the count and widen by one on both sides.
3. Return the total count.

## Code

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        res = 0

        for i in range(len(s)):
            res += self.countPali(s, i, i)
            res += self.countPali(s, i, i + 1)
        return res

    def countPali(self, s, l, r):
        res = 0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            res += 1
            l -= 1
            r += 1
        return res
```

## Complexity

- **Time:** `O(n^2)` — `2n - 1` centers, each expanding up to `O(n)`.
- **Space:** `O(1)` — constant extra variables.

## Other Approaches

- **2-D DP table:** `dp[i][j]` true if `s[i:j+1]` is a palindrome, count the trues — Time `O(n^2)`, Space `O(n^2)`.
- **Manacher's algorithm:** sum of `(radius + 1) // 2` over transformed centers — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Same center-expansion engine as Longest Palindromic Substring — here you count successful expansions instead of tracking the longest one.
