---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/encode-and-decode-strings/
neetcode: https://neetcode.io/problems/string-encode-and-decode
---
# Encode and Decode Strings

**Topic:** Arrays & Hashing · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/encode-and-decode-strings/) · [NeetCode](https://neetcode.io/problems/string-encode-and-decode)

## Problem

Design a pair of functions that convert a list of strings into a single string and back again, so the list can be transmitted as one string and reconstructed exactly on the other side. Implement the class `Codec` with:

- `encode(strs)`: takes a list of strings and returns one encoded string.
- `decode(s)`: takes a string produced by `encode` and returns the original list of strings.

The strings may contain any of the 256 ASCII characters (including delimiters you might be tempted to use, such as `#`, `,`, or spaces), may be empty, and the list itself may be empty. Do not rely on language serialization helpers such as `eval` or `pickle`. (This is a LeetCode Premium problem; on NeetCode it is called "String Encode and Decode".)

## Examples

**Example 1**
```text
Input: ["neet","code","love","you"]
Output: ["neet","code","love","you"]
Explanation: decode(encode(strs)) returns the original list.
```

**Example 2**
```text
Input: ["we","say",":","yes","#4#"]
Output: ["we","say",":","yes","#4#"]
```

**Example 3**
```text
Input: ["", ""]
Output: ["", ""]
```

## Constraints

- `0 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` may contain any of the 256 valid ASCII characters.
