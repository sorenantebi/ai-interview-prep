---
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/valid-palindrome-ii/
neetcode: https://neetcode.io/problems/valid-palindrome-ii
---
# Valid Palindrome II - Solution

## Intuition

Compare characters from both ends moving inward. As long as they match, nothing needs to change. At the first mismatch, the single allowed deletion must remove either the left or the right character of that pair, so we only need to check whether the remaining substring is a palindrome for each of those two choices.

## Approach

1. Place pointers `left = 0` and `right = len(s) - 1`.
2. While `left < right`, if `s[left] == s[right]`, move both inward.
3. On the first mismatch, return true if `s[left+1..right]` or `s[left..right-1]` is a palindrome.
4. If the pointers meet without a mismatch, the string is already a palindrome, so return true.

## Code

```python
class Solution:
    def validPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1
        
        while i < j:
            if s[i] == s[j]:
                i += 1
                j -= 1
            else:
                return self.validPalindromeUtil(s, i + 1, j) or self.validPalindromeUtil(s, i, j - 1)
        return True
    
    def validPalindromeUtil(self, s, i, j):
        while i < j:
            if s[i] == s[j]:
                i += 1
                j -= 1
            else:
                return False
        
        return True
```

## Complexity

- **Time:** `O(n)` — one pass for the main scan, plus at most two more linear scans after the single mismatch.
- **Space:** `O(1)` — only pointer variables are used; no substrings are copied.

## Other Approaches

- **Brute force:** try deleting each character and check whether the result is a palindrome — Time `O(n^2)` / Space `O(n)`
- **Recursion with a deletion counter:** recurse on the mismatch with a flag for whether a deletion was used — Time `O(n)` / Space `O(n)` for the call stack

## C++

```cpp
class Solution {
private:
    bool validPalindromeUtil(string s, int i, int j) {
        while(i < j)
            if(s[i] == s[j]) {
                i += 1;
                j -= 1;
            } else
                return false;
        return true;
    }
public:
    bool validPalindrome(string s) {
        int i = 0, j = s.length() - 1;
        
        while(i < j)
            if(s[i] == s[j]) {
                i += 1;
                j -= 1;
            } else
                return validPalindromeUtil(s, i + 1, j) || validPalindromeUtil(s, i, j - 1);
        return true;
    }
};
```
