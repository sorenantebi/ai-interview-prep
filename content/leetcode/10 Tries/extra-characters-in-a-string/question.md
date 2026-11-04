---
video: https://www.youtube.com/watch?v=ONstwO1cD7c
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/extra-characters-in-a-string/
neetcode: https://neetcode.io/problems/extra-characters-in-a-string
---
# Extra Characters in a String

**Topic:** Tries · **Difficulty:** Medium

## Problem

You are given a 0-indexed string `s` and a list of words `dictionary`. Break `s` into one or more non-overlapping substrings so that each substring appears in `dictionary`. Some characters of `s` may not belong to any chosen substring; these are the extra characters.

Return the minimum number of extra characters left over when `s` is broken up optimally.

## Examples

**Example 1**
```text
Input: s = "leetscode", dictionary = ["leet","code","leetcode"]
Output: 1
```
Explanation: Break `s` into "leet" (indices 0 to 3) and "code" (indices 5 to 8). Only the character at index 4 is unused, so the answer is 1.

**Example 2**
```text
Input: s = "sayhelloworld", dictionary = ["hello","world"]
Output: 3
```
Explanation: Break `s` into "hello" (indices 3 to 7) and "world" (indices 8 to 12). The characters at indices 0, 1, 2 are extra, so the answer is 3.

## Constraints

- `1 <= s.length <= 50`
- `1 <= dictionary.length <= 50`
- `1 <= dictionary[i].length <= 50`
- `dictionary[i]` and `s` consist of only lowercase English letters
- `dictionary` contains distinct words
