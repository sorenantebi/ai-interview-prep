---
topic: "String Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
---
# Find the Index of the First Occurrence in a String - Solution

## Intuition

A match of `needle` must start at some index `i` in `haystack` such that the next `len(needle)` characters equal `needle`. Checking every possible start is simple, but the Knuth-Morris-Pratt (KMP) algorithm avoids re-comparing characters after a mismatch by precomputing how much of the needle's prefix can be reused, giving linear time.

## Approach

1. Build the KMP failure table `lps` for `needle`, where `lps[i]` is the length of the longest proper prefix of `needle[:i+1]` that is also a suffix of it.
2. Scan `haystack` with index `i` while keeping `j`, the number of needle characters currently matched.
3. On a mismatch with `j > 0`, fall back with `j = lps[j - 1]` instead of restarting.
4. On a match, advance `j`.
5. When `j` equals `len(needle)`, return `i - j + 1`.
6. If the scan ends without a full match, return `-1`.

## Code

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if needle == "":
            return 0
        lps = [0] * len(needle)

        prevLPS, i = 0, 1
        while i < len(needle):
            if needle[i] == needle[prevLPS]:
                lps[i] = prevLPS + 1
                prevLPS += 1
                i += 1
            elif prevLPS == 0:
                lps[i] = 0
                i += 1
            else:
                prevLPS = lps[prevLPS - 1]

        i = 0  # ptr for haystack
        j = 0  # ptr for needle
        while i < len(haystack):
            if haystack[i] == needle[j]:
                i, j = i + 1, j + 1
            else:
                if j == 0:
                    i += 1
                else:
                    j = lps[j - 1]
            if j == len(needle):
                return i - len(needle)
        return -1
```

## Complexity

- **Time:** `O(n + m)` — building the table takes `O(m)`, and the scan takes `O(n)` because `j` increases at most once per character and every fallback decreases it, so total fallbacks are bounded by total increments.
- **Space:** `O(m)` — the failure table has one entry per needle character.

## Other Approaches

- **Brute force:** try every start index and compare up to `m` characters — Time `O(n * m)` / Space `O(1)`
- **Built-in `str.find`:** one-line call that does the same search — Time depends on implementation, worst case `O(n * m)` / Space `O(1)`
- **Rabin-Karp:** compare rolling hashes of each window to the needle's hash, verifying on hash match — Time `O(n + m)` average, `O(n * m)` worst case / Space `O(1)`

## C++

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        if(haystack.size()<needle.size()) return -1;
        int found=0;
        for(int i=0;i<haystack.size()-needle.size()+1;i++){
            if(haystack[i]==needle[0]){
                found=1;
                for(int j=1;j<needle.size();j++){
                    if(haystack[i+j]!=needle[j]){
                        found=0;break;
                    }
                }if(found==1) return i;
            }
        }return -1;
    }
};
```
