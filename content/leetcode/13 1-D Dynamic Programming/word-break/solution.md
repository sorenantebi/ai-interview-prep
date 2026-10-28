---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/word-break/
neetcode: https://neetcode.io/problems/word-break
---
# Word Break - Solution

**Question:** Word Break - Question · **Difficulty:** Medium

## Intuition

`dp[i]` is true when the prefix `s[:i]` can be segmented. The prefix `s[:i]` is breakable if some dictionary word `w` ends exactly at `i` and the part before it, `s[:i - len(w)]`, is breakable. Since words are at most 20 characters long, we only need to check the matching words, not every split point.

## Approach

1. `dp[0] = True` (empty prefix); the rest `False`.
2. For each `i` from 1 to `n`, for each word `w` in the dictionary: if `len(w) <= i`, `dp[i - len(w)]` is true, and `s[i - len(w):i] == w`, set `dp[i] = True` and stop.
3. Return `dp[n]`.

## Code

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:

        dp = [False] * (len(s) + 1)
        dp[len(s)] = True

        for i in range(len(s) - 1, -1, -1):
            for w in wordDict:
                if (i + len(w)) <= len(s) and s[i : i + len(w)] == w:
                    dp[i] = dp[i + len(w)]
                if dp[i]:
                    break

        return dp[0]
```

## Complexity

- **Time:** `O(n · m · k)` — `n` positions, `m` words, up to `k` (max word length) characters compared each.
- **Space:** `O(n)` — the DP array (word list is input).

## Other Approaches

- **Split-point DP with a word set:** for each `i`, try every `j < i` (or `j >= i - maxLen`) and check `s[j:i] in word_set` — Time `O(n · L^2)` with `L = max word length`, Space `O(n + total dict size)`.
- **Trie + DP / BFS over indices:** walk a trie from each reachable index — Time `O(n · L)`, Space `O(total dict size)`.

## Key Takeaway

Segmentation problems are prefix DPs: `dp[i]` = "can the first `i` characters be built", transitioning on the last piece.

## C++

```cpp
/*
    Given a string & dictionary, return true if:
    Can segment string into 1 or more dictionary words

    DP, at each loop, substring, check if in dict, & store

    Time: O(n^3)
    Space: O(n)
*/

class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> words;
        for (int i = 0; i < wordDict.size(); i++) {
            words.insert(wordDict[i]);
        }
        
        int n = s.size();
        vector<bool> dp(n + 1);
        dp[0] = true;
        
        for (int i = 1; i <= n; i++) {
            for (int j = i - 1; j >= 0; j--) {
                if (dp[j]) {
                    string word = s.substr(j, i - j);
                    if (words.find(word) != words.end()) {
                        dp[i] = true;
                        break;
                    }
                }
            }
        }
        
        return dp[n];
    }
};
```
