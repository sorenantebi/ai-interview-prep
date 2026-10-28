---
topic: "2-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/distinct-subsequences/
neetcode: https://neetcode.io/problems/count-subsequences
---
# Distinct Subsequences - Solution

**Question:** Distinct Subsequences - Question · **Difficulty:** Hard

## Intuition

Let `dp[j]` = number of ways the processed prefix of `s` can form `t[:j]`. When we read a new character `c` of `s`, every `j` with `t[j-1] == c` gains `dp[j-1]` new ways (use `c` as the `j`-th char of `t`); skipping `c` keeps the old count. Iterating `j` **backwards** ensures each `s` character is used at most once per subsequence.

## Approach

1. `dp = [1] + [0] * len(t)` — the empty `t` is formed in exactly one way.
2. For each character `c` of `s`, for `j` from `len(t)` down to 1: if `t[j-1] == c`, `dp[j] += dp[j-1]`.
3. Return `dp[len(t)]`.

## Code

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        cache = {}

        for i in range(len(s) + 1):
            cache[(i, len(t))] = 1
        for j in range(len(t)):
            cache[(len(s), j)] = 0

        for i in range(len(s) - 1, -1, -1):
            for j in range(len(t) - 1, -1, -1):
                if s[i] == t[j]:
                    cache[(i, j)] = cache[(i + 1, j + 1)] + cache[(i + 1, j)]
                else:
                    cache[(i, j)] = cache[(i + 1, j)]
        return cache[(0, 0)]
```

## Complexity

- **Time:** `O(m * n)` — `m = len(s)`, `n = len(t)`.
- **Space:** `O(n)` — one row indexed by `t` prefix length.

## Other Approaches

- **2-D DP `dp[i][j]`:** `dp[i][j] = dp[i+1][j] + (s[i]==t[j]) * dp[i+1][j+1]` — Time `O(mn)`, Space `O(mn)`.
- **Memoized DFS on `(i, j)`:** skip or use `s[i]` — Time `O(mn)`, Space `O(mn)`.

## Key Takeaway

Counting subsequence embeddings: each source char either skips or matches; a reverse inner loop gives the 0/1 "use once" semantics in a 1-D table.

## C++

```cpp
/*
    Given 2 strings s & t:
    Return # of distinct subsequences of s which equals t
    Ex. s = "rabbbit", t = "rabbit" -> 3, RABBbIT, RAbBBIT, RABbBIT

    DFS + memo, cache on i & j indices to the # of distinct subseq
    2 choices: if chars equal, look at remainder of both s & t
               if chars not equal, only look at remainder of s

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int numDistinct(string s, string t) {
        return dfs(s, t, 0, 0);
    }
private:
    // {(i, j) -> # of distinct subsequences}
    map<pair<int, int>, int> dp;
    
    int dfs(string& s, string& t, int i, int j) {
        if (j == t.size()) {
            return 1;
        }
        if (i == s.size()) {
            return 0;
        }
        if (dp.find({i, j}) != dp.end()) {
            return dp[{i, j}];
        }
        
        if (s[i] == t[j]) {
            dp[{i, j}] = dfs(s, t, i + 1, j + 1) + dfs(s, t, i + 1, j);
        } else {
            dp[{i, j}] = dfs(s, t, i + 1, j);
        }
        return dp[{i, j}];
    }
};
```
