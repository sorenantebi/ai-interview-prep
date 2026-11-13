---
topic: "String Manipulation"
difficulty: Hard
leetcode: https://leetcode.com/problems/text-justification/
---
# Text Justification

**Topic:** String Manipulation · **Difficulty:** Hard

## Problem

Given an array of strings `words` and an integer `maxWidth`, format the text so that every line has exactly `maxWidth` characters and is fully justified (both left and right).

Pack words greedily: place as many words as fit on each line. Pad with extra spaces `' '` where needed so each line is exactly `maxWidth` characters long.

Extra spaces between words must be distributed as evenly as possible. If the spaces do not divide evenly among the gaps, the gaps on the left receive more spaces than the gaps on the right.

The last line of text must be left-justified: words are separated by a single space, and the remaining spaces are placed at the end of the line.

Notes:

- A word is a sequence of non-space characters.
- Each word's length is greater than 0 and at most `maxWidth`.
- The input array contains at least one word.

## Examples

**Example 1**
```text
Input: words = ["This", "is", "an", "example", "of", "text", "justification."], maxWidth = 16
Output:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]
```

**Example 2**
```text
Input: words = ["What","must","be","acknowledgment","shall","be"], maxWidth = 16
Output:
[
  "What   must   be",
  "acknowledgment  ",
  "shall be        "
]
Explanation: The last line is "shall be        " instead of "shall     be", because the last line must be left-justified.
A line containing only one word is also left-justified, as with the second line.
```

**Example 3**
```text
Input: words = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"], maxWidth = 20
Output:
[
  "Science  is  what we",
  "understand      well",
  "enough to explain to",
  "a  computer.  Art is",
  "everything  else  we",
  "do                  "
]
```

## Constraints

- `1 <= words.length <= 300`
- `1 <= words[i].length <= 20`
- `words[i]` consists of only English letters and symbols.
- `1 <= maxWidth <= 100`
- `words[i].length <= maxWidth`
