---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/longest-common-prefix/
neetcode: https://neetcode.io/problems/longest-common-prefix
---
# Longest Common Prefix - Solution

## Intuition

The common prefix can never be longer than the shortest string, and it is determined character by character: the prefix ends at the first column where any string disagrees with the first string (or runs out of characters).

## Approach

1. Take the first string as the reference.
2. For each index `i` in the reference, compare `strs[0][i]` with the character at position `i` of every other string.
3. If another string is too short or its character differs, return `strs[0][:i]`.
4. If the loop finishes, the whole first string is a common prefix, so return it.

## Code

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        for i in range(len(strs[0])):
            for s in strs:
                if i >= len(s) or s[i] != strs[0][i]:
                    return strs[0][:i]
        return strs[0]
```

## Complexity

- **Time:** `O(S)` — `S` is the total number of characters across all strings; in the worst case every character is compared once.
- **Space:** `O(1)` — only indices are kept, apart from the returned slice.

## Other Approaches

- **Sorting:** sort the array, then compare only the first and last strings, since they differ the most — Time `O(S log n)` / Space `O(1)` extra
- **Horizontal scanning:** keep a running prefix and shorten it against each string in turn — Time `O(S)` / Space `O(1)`
- **Trie:** insert all strings and walk down while a node has exactly one child and is not a word end — Time `O(S)` / Space `O(S)`
- **Binary search on length:** binary search the prefix length and check it against all strings — Time `O(S log m)` / Space `O(1)`

## C++

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        string result = strs[0];
        int charIndex = 0;
        
        //finding minimum string length  - that could be max common prefix
        long maxCharIndex = strs[0].length();
        for (int i = 1; i < strs.size(); ++i) {
            if (strs[i].length() < maxCharIndex) {
                maxCharIndex = strs[i].length();
            }
        }

        while (charIndex < maxCharIndex) {
            char prevChar = strs[0][charIndex];
            for (int i = 1; i < strs.size(); ++i) {
                if (prevChar == strs[i][charIndex]) {
                    continue;
                }
                return result.substr(0, charIndex);
            }
            ++charIndex;
            result += prevChar;
        }
        return result.substr(0, charIndex);
    }
};
```
