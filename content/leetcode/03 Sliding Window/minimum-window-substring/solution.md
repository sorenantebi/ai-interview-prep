---
topic: "Sliding Window"
difficulty: Hard
leetcode: https://leetcode.com/problems/minimum-window-substring/
neetcode: https://neetcode.io/problems/minimum-window-with-characters
---
# Minimum Window Substring - Solution

**Question:** Minimum Window Substring - Question · **Difficulty:** Hard

## Intuition

Use a variable sliding window. Expand the right edge until the window contains all required characters, then shrink from the left as much as possible while it stays valid, recording the smallest valid window. A counter `have` of how many distinct characters currently meet their required count lets us test validity in `O(1)`.

## Approach

1. Build `need = Counter(t)`; `required = len(need)`; `have = 0`; `window = {}`.
2. For each `r`, add `s[r]` to `window`; if its count just reached `need[s[r]]`, increment `have`.
3. While `have == required`:
   - Record the window if it is the smallest so far.
   - Remove `s[l]` from `window`; if its count dropped below `need[s[l]]`, decrement `have`. Move `l` right.
4. Return the best window, or `""` if none was found.

## Code

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""

        countT, window = {}, {}
        for c in t:
            countT[c] = 1 + countT.get(c, 0)

        have, need = 0, len(countT)
        res, resLen = [-1, -1], float("infinity")
        l = 0
        for r in range(len(s)):
            c = s[r]
            window[c] = 1 + window.get(c, 0)

            if c in countT and window[c] == countT[c]:
                have += 1

            while have == need:
                # update our result
                if (r - l + 1) < resLen:
                    res = [l, r]
                    resLen = r - l + 1
                # pop from the left of our window
                window[s[l]] -= 1
                if s[l] in countT and window[s[l]] < countT[s[l]]:
                    have -= 1
                l += 1
        l, r = res
        return s[l : r + 1] if resLen != float("infinity") else ""
```

## Complexity

- **Time:** `O(m + n)` — building `need` is `O(n)`; each index of `s` enters and leaves the window once.
- **Space:** `O(k)` — `k` distinct characters in the maps (at most 52 letters here).

## Other Approaches

- **Brute force:** check every substring against `Counter(t)` — Time `O(m^2 * k)`, Space `O(k)`.
- **Filtered s:** run the same window only over positions of `s` whose characters occur in `t` — same worst case, faster when `t` is much smaller than the alphabet of `s`.

## Key Takeaway

Minimum-window problems = expand until valid, then shrink while valid. Track "number of satisfied distinct characters" instead of comparing full maps to keep each step `O(1)`.

## C++

```cpp
/*
    Given 2 strings s & t, return min window substring
    of s such that all chars in t are included in window
    Ex. s = "ADOBECODEBANC" t = "ABC" -> "BANC"

    Sliding window + hash map {char -> count}
    Move j until valid, move i to find smaller

    Time: O(m + n)
    Space: O(m + n)
*/

class Solution {
public:
    string minWindow(string s, string t) {
        // count of char in t
        unordered_map<char, int> m;
        for (int i = 0; i < t.size(); i++) {
            m[t[i]]++;
        }
        
        int i = 0;
        int j = 0;
        
        // # of chars in t that must be in s
        int counter = t.size();
        
        int minStart = 0;
        int minLength = INT_MAX;
        
        while (j < s.size()) {
            // if char in s exists in t, decrease
            if (m[s[j]] > 0) {
                counter--;
            }
            // if char doesn't exist in t, will be -'ve
            m[s[j]]--;
            // move j to find valid window
            j++;
            
            // when window found, move i to find smaller
            while (counter == 0) {
                if (j - i < minLength) {
                    minStart = i;
                    minLength = j - i;
                }
                
                m[s[i]]++;
                // when char exists in t, increase
                if (m[s[i]] > 0) {
                    counter++;
                }
                i++;
            }
        }
        
        if (minLength != INT_MAX) {
            return s.substr(minStart, minLength);
        }
        return "";
    }
};
```
