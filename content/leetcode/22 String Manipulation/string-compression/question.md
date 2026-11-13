---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/string-compression/
---
# String Compression

**Topic:** String Manipulation · **Difficulty:** Medium

## Problem

You are given an array of characters `chars`. Compress it in place using the following rules.

Start with an empty string `s`. For each group of consecutive repeating characters in `chars`:

- If the group has length 1, append the character to `s`.
- Otherwise, append the character followed by the group's length.

The compressed string `s` is not returned separately. Instead, it must be stored in the input array `chars`. Group lengths of 10 or more are split into multiple characters (for example, a length of 12 is written as `"1"` then `"2"`).

After modifying the array, return its new length. Your algorithm must use only constant extra space.

Characters in the array beyond the returned length do not matter and should be ignored.

## Examples

**Example 1**
```text
Input: chars = ["a","a","b","b","c","c","c"]
Output: 6
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".
The first 6 characters of chars become ["a","2","b","2","c","3"].
```

**Example 2**
```text
Input: chars = ["a"]
Output: 1
Explanation: The only group is "a", which stays uncompressed because it has length 1.
The first character of chars is ["a"].
```

**Example 3**
```text
Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: 4
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
The first 4 characters of chars become ["a","b","1","2"].
```

## Constraints

- `1 <= chars.length <= 2000`
- `chars[i]` is a lowercase English letter, uppercase English letter, digit, or symbol.
