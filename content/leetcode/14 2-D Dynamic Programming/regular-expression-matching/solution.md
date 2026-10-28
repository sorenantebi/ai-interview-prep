---
topic: "2-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/regular-expression-matching/
neetcode: https://neetcode.io/problems/regular-expression-matching
---
# Regular Expression Matching - Solution

**Question:** Regular Expression Matching - Question · **Difficulty:** Hard

## Intuition

Let `dp[i][j]` = "does `s[i:]` match `p[j:]`?". If the next pattern token is `x*`, we can either skip it entirely (`dp[i][j+2]`) or, if `s[i]` matches `x`, consume one character of `s` and stay on the same token (`dp[i+1][j]`). Otherwise the current characters must match and both advance (`dp[i+1][j+1]`). Filling from the end gives a bottom-up DP.

## Approach

1. Create `dp` of size `(m+1) x (n+1)` with `dp[m][n] = True` (empty matches empty).
2. Iterate `i` from `m` down to 0 and `j` from `n - 1` down to 0:
   - `first = i < m and p[j] in (s[i], '.')`.
   - If `j + 1 < n and p[j+1] == '*'`: `dp[i][j] = dp[i][j+2] or (first and dp[i+1][j])`.
   - Else: `dp[i][j] = first and dp[i+1][j+1]`.
3. Return `dp[0][0]`.

## Code

```python
# BOTTOM-UP Dynamic Programming
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        cache = [[False] * (len(p) + 1) for i in range(len(s) + 1)]
        cache[len(s)][len(p)] = True

        for i in range(len(s), -1, -1):
            for j in range(len(p) - 1, -1, -1):
                match = i < len(s) and (s[i] == p[j] or p[j] == ".")

                if (j + 1) < len(p) and p[j + 1] == "*":
                    cache[i][j] = cache[i][j + 2]
                    if match:
                        cache[i][j] = cache[i + 1][j] or cache[i][j]
                elif match:
                    cache[i][j] = cache[i + 1][j + 1]

        return cache[0][0]


# TOP DOWN MEMOIZATION
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        cache = {}

        def dfs(i, j):
            if (i, j) in cache:
                return cache[(i, j)]
            if i >= len(s) and j >= len(p):
                return True
            if j >= len(p):
                return False

            match = i < len(s) and (s[i] == p[j] or p[j] == ".")
            if (j + 1) < len(p) and p[j + 1] == "*":
                cache[(i, j)] = dfs(i, j + 2) or (  # dont use *
                    match and dfs(i + 1, j)
                )  # use *
                return cache[(i, j)]
            if match:
                cache[(i, j)] = dfs(i + 1, j + 1)
                return cache[(i, j)]
            cache[(i, j)] = False
            return False

        return dfs(0, 0)
```

## Complexity

- **Time:** `O(m * n)` — each `(i, j)` state is computed in `O(1)`.
- **Space:** `O(m * n)` — the DP table (reducible to `O(n)` with two rows).

## Other Approaches

- **Top-down memoized recursion on `(i, j)`:** same transitions, often easier to write in an interview — Time `O(mn)`, Space `O(mn)`.
- **Plain backtracking:** without memoization, patterns like `a*a*a*...` cause exponential blow-up — Time exponential, Space `O(m + n)`.

## Key Takeaway

Treat `x*` as one token with two choices — "zero more copies" (skip the token) or "one more copy" (consume a char, keep the token) — and memoize on `(i, j)`.

## C++

```cpp
/*
    Given string & pattern, implement RegEx matching
    '.' -> matches any single character
    '*' -> matches zero or more of the preceding element
    Matching should cover the entire input string (not partial)
    Ex. s = "aa", p = "a" -> false, "a" doesn't match entire string "aa"

    DFS + memo, 2 choices at a *: either use it, or don't use it

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    bool isMatch(string s, string p) {
        return dfs(s, p, 0, 0);
    }
private:
    map<pair<int, int>, bool> dp;
    
    bool dfs(string& s, string& p, int i, int j) {
        if (dp.find({i, j}) != dp.end()) {
            return dp[{i, j}];
        }
        
        if (i >= s.size() && j >= p.size()) {
            return true;
        }
        if (j >= p.size()) {
            return false;
        }
        
        bool match = i < s.size() && (s[i] == p[j] || p[j] == '.');
        if (j + 1 < p.size() && p[j + 1] == '*') {
            // choices: either (1) don't use *, or (2) use *
            dp[{i, j}] = dfs(s, p, i, j + 2) || (match && dfs(s, p, i + 1, j));
            return dp[{i, j}];
        }
        
        if (match) {
            dp[{i, j}] = dfs(s, p, i + 1, j + 1);
            return dp[{i, j}];
        }
        
        dp[{i, j}] = false;
        return dp[{i, j}];
    }
};
```
