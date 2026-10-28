---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/partition-labels/
neetcode: https://neetcode.io/problems/partition-labels
---
# Partition Labels - Solution

**Question:** Partition Labels - Question · **Difficulty:** Medium

## Intuition

A part that contains letter `c` must extend at least to the **last** occurrence of `c`. Scan left to right, stretching the current part's end to the last occurrence of each letter seen; when the scan index reaches that end, no letter inside the part appears later, so we can cut there.

## Approach

1. Record `last[c]` = last index of each character.
2. Keep `start = 0`, `end = 0`. For each index `i`: `end = max(end, last[s[i]])`.
3. If `i == end`, append `end - start + 1` to the result and set `start = i + 1`.
4. Return the result.

## Code

```python
class Solution:
    def partitionLabels(self, S: str) -> List[int]:
        count = {}
        res = []
        i, length = 0, len(S)
        for j in range(length):
            c = S[j]
            count[c] = j

        curLen = 0
        goal = 0
        while i < length:
            c = S[i]
            goal = max(goal, count[c])
            curLen += 1

            if goal == i:
                res.append(curLen)
                curLen = 0
            i += 1
        return res
```

## Complexity

- **Time:** `O(n)` — two linear passes.
- **Space:** `O(1)` — at most 26 entries in `last` (output excluded).

## Other Approaches

- **Merge intervals:** build `[first, last]` for each letter and merge overlapping intervals; the merged lengths are the answer — Time `O(n)` (26 intervals to sort), Space `O(1)`.

## Key Takeaway

"Each item in one group" partitioning = extend the current window to the furthest last-occurrence; cut when the index catches up.

## C++

```cpp
/*
    Partition string so each letter appears in at most 1 part, return sizes
    Ex. s = "ababcbacadefegdehijhklij" -> [9,7,8]

    Greedy: determine last occurrence of each char, then loop thru & get sizes

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> partitionLabels(string s) {
        int n = s.size();
        // {char -> last index in s}
        vector<int> lastIndex(26);
        for (int i = 0; i < n; i++) {
            lastIndex[s[i] - 'a'] = i;
        }
        
        int size = 0;
        int end = 0;
        
        vector<int> result;
        
        for (int i = 0; i < n; i++) {
            size++;
            // constantly checking for further indices if possible
            end = max(end, lastIndex[s[i] - 'a']);
            if (i == end) {
                result.push_back(size);
                size = 0;
            }
        }
        
        return result;
    }
};
```
