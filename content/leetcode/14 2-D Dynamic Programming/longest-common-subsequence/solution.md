---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-common-subsequence/
neetcode: https://neetcode.io/problems/longest-common-subsequence
---
# Longest Common Subsequence - Solution

**Question:** Longest Common Subsequence - Question · **Difficulty:** Medium

## Intuition

Compare prefixes. If the last characters of `text1[:i]` and `text2[:j]` match, they can both end the LCS, giving `1 + LCS(i-1, j-1)`. Otherwise one of them is unused, giving `max(LCS(i-1, j), LCS(i, j-1))`. This is a classic 2-D DP that can be rolled into one row.

## Approach

1. Let `dp[j]` hold the LCS of the current prefix of `text1` with `text2[:j]`; start with all zeros.
2. For each character `a` of `text1`, sweep `j` from 1 to `len(text2)`, keeping `prev` = the old `dp[j-1]` (the diagonal value):
   - If `a == text2[j-1]`: `dp[j] = prev + 1`.
   - Else: `dp[j] = max(dp[j], dp[j-1])`.
3. Return `dp[-1]`.

## Code

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        dp = [[0 for j in range(len(text2) + 1)] for i in range(len(text1) + 1)]

        for i in range(len(text1) - 1, -1, -1):
            for j in range(len(text2) - 1, -1, -1):
                if text1[i] == text2[j]:
                    dp[i][j] = 1 + dp[i + 1][j + 1]
                else:
                    dp[i][j] = max(dp[i][j + 1], dp[i + 1][j])

        return dp[0][0]
```

## Complexity

- **Time:** `O(m * n)` — every pair of prefix lengths is evaluated once.
- **Space:** `O(min(m, n))` — one row over the shorter string.

## Other Approaches

- **Full 2-D table:** `dp[i][j]` over all prefix pairs; also lets you reconstruct the subsequence — Time `O(mn)`, Space `O(mn)`.
- **Memoized recursion on `(i, j)`:** same recurrence top-down — Time `O(mn)`, Space `O(mn)` plus recursion stack.

## Key Takeaway

Two-sequence DP: index the state by a prefix of each string; match -> diagonal + 1, mismatch -> best of dropping one character. When rolling into 1-D, save the diagonal before overwriting.

## C++

```cpp
/*
    Given 2 strings, return length of longest common subsequence
    Ex. text1 = "abcde", text2 = "ace" -> 3, "ace" is LCS

                j
            a   c   e
        a   3
        b       2     --> visualization of below, build DP bottom-up
    i   c       2
        d           1
        e           1

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.size();
        int n = text2.size();
        
        vector<vector<int>> dp(m + 1, vector<int>(n + 1));
        
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                if (text1[i] == text2[j]) {
                    dp[i][j] = 1 + dp[i + 1][j + 1];
                } else {
                    dp[i][j] = max(dp[i + 1][j], dp[i][j + 1]);
                }
            }
        }
        
        return dp[0][0];
    }
};
```
