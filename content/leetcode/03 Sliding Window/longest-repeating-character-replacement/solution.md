---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-repeating-character-replacement/
neetcode: https://neetcode.io/problems/longest-repeating-substring-with-replacement
---
# Longest Repeating Character Replacement - Solution

**Question:** Longest Repeating Character Replacement - Question · **Difficulty:** Medium

## Intuition

A window can be made uniform iff `window_length - count_of_most_frequent_char <= k`. Slide a window, counting characters, and shrink from the left when this fails. We only need the best `maxf` ever seen: the answer can only grow when `maxf` grows, so a stale (too large) `maxf` never produces a wrong larger answer.

## Approach

1. Keep `count` per letter, `l = 0`, `maxf = 0`, `best = 0`.
2. For each `r`:
   - Increment `count[s[r]]`, update `maxf = max(maxf, count[s[r]])`.
   - If `(r - l + 1) - maxf > k`, decrement `count[s[l]]` and move `l` right by one.
   - Update `best = max(best, r - l + 1)`.
3. Return `best`.

## Code

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        
        l = 0
        maxf = 0
        for r in range(len(s)):
            count[s[r]] = 1 + count.get(s[r], 0)
            maxf = max(maxf, count[s[r]])

            if (r - l + 1) - maxf > k:
                count[s[l]] -= 1
                l += 1

        return (r - l + 1)
```

## Complexity

- **Time:** `O(n)` — each index enters and leaves the window at most once.
- **Space:** `O(1)` — at most 26 counters.

## Other Approaches

- **Recompute max each step:** use `max(count.values())` instead of the historical `maxf` and shrink with a `while` loop — Time `O(26n)`, Space `O(1)`; easier to reason about.
- **Per-letter windows:** for each of the 26 letters, find the longest window with at most `k` other letters — Time `O(26n)`, Space `O(1)`.

## Key Takeaway

For "longest window that can be fixed with k changes", the validity test is `len - maxFreq <= k`; never decreasing `maxf` is a safe optimization because only a larger `maxf` can improve the answer.

## C++

```cpp
/*
    Given a string s & an int k, can change any char k times:
    Return length of longest substring containing same letter
    Ex. s = "ABAB" k = 2 -> 4 "AAAA", s = "AABABBA" k = 1 -> 4

    Sliding window, expand if can change char, contract if > k

    Time: O(n)
    Space: O(26)
*/

class Solution {
public:
    int characterReplacement(string s, int k) {
        vector<int> count(26);
        int maxCount = 0;
        
        int i = 0;
        int j = 0;
        
        int result = 0;
        
        while (j < s.size()) {
            count[s[j] - 'A']++;
            maxCount = max(maxCount, count[s[j] - 'A']);
            if (j - i + 1 - maxCount > k) {
                count[s[i] - 'A']--;
                i++;
            }
            result = max(result, j - i + 1);
            j++;
        }
        
        return result;
    }
};
```
