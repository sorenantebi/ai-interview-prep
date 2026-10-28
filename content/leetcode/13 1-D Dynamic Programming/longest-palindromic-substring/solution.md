---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-palindromic-substring/
neetcode: https://neetcode.io/problems/longest-palindromic-substring
---
# Longest Palindromic Substring - Solution

**Question:** Longest Palindromic Substring - Question · **Difficulty:** Medium

## Intuition

Every palindrome mirrors around a center, which is either a single character (odd length) or a gap between two characters (even length). There are only `2n - 1` centers, and from each we can expand outward while the characters match, so we find the longest palindrome in `O(n^2)` time with `O(1)` extra space.

## Approach

1. For every index `i`, expand around `(i, i)` and around `(i, i + 1)`.
2. Expansion: while `l >= 0`, `r < n` and `s[l] == s[r]`, move `l` left and `r` right; the palindrome is `s[l + 1 : r]`.
3. Track the start and length of the longest palindrome found; return that slice.

## Code

```python

class Solution:
    def longestPalindrome(self, s: str) -> str:
        self.res = ""
        self.lenres = 0
        for i in range(len(s)):
            s1 = self.helper(s, i, i)
            s2 = self.helper(s, i, i + 1)
        return s2
        
    def helper(self, s, left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                if (right - left + 1) > self.lenres:
                    self.res = s[left:right+1]
                    self.lenres = right - left + 1
                left -= 1
                right += 1
            return self.res
```

## Complexity

- **Time:** `O(n^2)` — `2n - 1` centers, each expanding up to `O(n)`.
- **Space:** `O(1)` — only indices (excluding the output slice).

## Other Approaches

- **2-D DP table:** `dp[i][j] = s[i] == s[j] and dp[i+1][j-1]` — Time `O(n^2)`, Space `O(n^2)`.
- **Manacher's algorithm:** reuses mirror information to get linear time — Time `O(n)`, Space `O(n)`.

## Key Takeaway

For palindromic substrings, "expand around center" (both odd and even centers) is the simplest optimal-in-practice technique; mention Manacher's for `O(n)`.

## C++

```cpp
/*
    Given a string s, return the longest palindromic substring in s
    Ex. s = "babad" -> "bab", s = "cbbd" -> "bb"

    Expand around center, extend as far as possible, store max length

    Time: O(n^2)
    Space: O(1)
*/

class Solution {
public:
    string longestPalindrome(string s) {
        int maxStart = 0;
        int maxLength = 1;
        
        for (int i = 0; i < s.size() - 1; i++) {
            middleOut(s, i, i, maxStart, maxLength);
            middleOut(s, i, i + 1, maxStart, maxLength);
        }
        
        return s.substr(maxStart, maxLength);
    }
private:
    void middleOut(string s, int i, int j, int& maxStart, int& maxLength) {
        while (i >= 0 && j <= s.size() - 1 && s[i] == s[j]) {
            i--;
            j++;
        }
        if (j - i - 1 > maxLength) {
            maxStart = i + 1;
            maxLength = j - i - 1;
        }
    }
};
```
