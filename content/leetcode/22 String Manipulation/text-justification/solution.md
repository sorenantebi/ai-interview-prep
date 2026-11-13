---
topic: "String Manipulation"
difficulty: Hard
leetcode: https://leetcode.com/problems/text-justification/
---
# Text Justification - Solution

## Intuition

This is a simulation problem. Greedily choose which words go on each line, then build each line according to one of two rules: full justification (spread spaces over the gaps) or left justification (last line, or a line with a single word). The difficulty lies in the details, not in the algorithm.

## Approach

1. Scan the words with an index `i`. For each line, extend `j` from `i` while the words plus one minimum space between each pair still fit within `maxWidth`.
2. Let `count = j - i` be the number of words on the line and `gaps = count - 1`.
3. If this is the last line (`j == len(words)`) or `gaps == 0`, left-justify: join with single spaces and pad the end with spaces up to `maxWidth`.
4. Otherwise compute `total_spaces = maxWidth - sum(word lengths)`. Each gap gets `total_spaces // gaps` spaces, and the leftmost `total_spaces % gaps` gaps get one extra.
5. Append the line to the result and continue from `i = j`.

## Code

```python
class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res = []
        line = []  # Words in current line
        length = 0  # Current line length
        i = 0
        while i < len(words):
            if length + len(line) + len(words[i]) > maxWidth:
                # Line complete
                extra_space = maxWidth - length
                word_cnt = len(line) - 1
                spaces = extra_space // max(1, word_cnt)
                remainder = extra_space % max(1, word_cnt)

                for j in range(max(1, len(line) - 1)):
                    line[j] += " " * spaces
                    if remainder:
                        line[j] += " "
                        remainder -= 1

                res.append("".join(line))
                line, length = [], 0  # Reset line and length
            
            line.append(words[i])
            length += len(words[i])
            i += 1

        # Handling the last line
        last_line = " ".join(line)
        trail_spaces = maxWidth - len(last_line)
        res.append(last_line + (trail_spaces * " "))

        return res
```

## Complexity

- **Time:** `O(S)` — where `S` is the total number of characters across all words (plus padding); each word is examined a constant number of times and each output line is built in time proportional to its length.
- **Space:** `O(maxWidth)` — extra space beyond the output is only the current line being built (the output itself takes `O(S)`).

## Other Approaches

- **Line-by-line with a running list:** accumulate words in a buffer and flush when the next word does not fit, then format the buffer — Time `O(S)` / Space `O(maxWidth)` extra.
- **Round-robin space distribution:** place single spaces between words, then hand out remaining spaces one gap at a time from the left in a loop — Time `O(S)` / Space `O(maxWidth)` extra.
