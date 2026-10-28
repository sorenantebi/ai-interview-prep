---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/edit-distance/
neetcode: https://neetcode.io/problems/edit-distance
---
# Edit Distance - Solution

**Question:** Edit Distance - Question · **Difficulty:** Medium

## Intuition

Let `dp[i][j]` be the edit distance between `word1[:i]` and `word2[:j]`. If the last characters match, no operation is needed: `dp[i-1][j-1]`. Otherwise take `1 +` the best of delete (`dp[i-1][j]`), insert (`dp[i][j-1]`), or replace (`dp[i-1][j-1]`). Base cases: converting to/from an empty string costs its length.

## Approach

1. `prev = list(range(n + 1))` is row `i = 0` (insert `j` characters).
2. For each `i` from 1 to `m`, build `cur` with `cur[0] = i` (delete `i` characters), then fill `cur[j]` with the recurrence using `prev[j-1]`, `prev[j]`, `cur[j-1]`.
3. After all rows, return `prev[n]`.

## Code

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        dp = [[float("inf")] * (len(word2) + 1) for i in range(len(word1) + 1)]

        for j in range(len(word2) + 1):
            dp[len(word1)][j] = len(word2) - j
        for i in range(len(word1) + 1):
            dp[i][len(word2)] = len(word1) - i

        for i in range(len(word1) - 1, -1, -1):
            for j in range(len(word2) - 1, -1, -1):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i + 1][j + 1]
                else:
                    dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j + 1], dp[i + 1][j + 1])
        return dp[0][0]
```

## Complexity

- **Time:** `O(m * n)` — each prefix pair evaluated once.
- **Space:** `O(n)` — two rows.

## Other Approaches

- **Full 2-D table:** same recurrence; allows backtracking the actual edit script — Time `O(mn)`, Space `O(mn)`.
- **Memoized recursion on `(i, j)`:** top-down version — Time `O(mn)`, Space `O(mn)` plus recursion stack.

## Key Takeaway

Edit distance is the template for two-string alignment DPs: match -> diagonal, mismatch -> 1 + min(up, left, diagonal).

## C++

```cpp
/*
    Given 2 strings, return minimum number of operations to convert word1 to word2

    Naive: check all possible edit sequences & choose shortest one
    Optimal: DP, if chars at i & j same, no operations needed, else 3 cases:
    (1) replace (i - 1, j - 1), (2) delete (i - 1, j), (3) insert (i, j - 1)

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int minDistance(string word1, string word2) {
        if (word1.empty() && word2.empty()) {
            return 0;
        }
        if (word1.empty() || word2.empty()) {
            return word1.size() + word2.size();  // all inserts or all deletes
        }
        
        int m = word1.size();
        int n = word2.size();
        
        vector<vector<int>> dp(m + 1, vector<int>(n + 1));
        
        // base cases (convert to empty string w/ deletions), dist is just length
        for (int i = 1; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 1; j <= n; j++) {
            dp[0][j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] == word2[j - 1]) {
                    // no operation needed, same char
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    // min(replace, delete, insert) + 1 <-- since an op was needed
                    dp[i][j] = min(dp[i - 1][j - 1], min(dp[i - 1][j], dp[i][j - 1])) + 1;
                }
            }
        }
        
        return dp[m][n];
    }
};

// Since we only need at most dp[i - 1][j - 1], can space optimize to O(n)
// class Solution {
// public:
//     int minDistance(string word1, string word2) {
//         int m = word1.size();
//         int n = word2.size();
//         int prev = 0;
//         vector<int> curr(n + 1);
//         for (int j = 1; j <= n; j++) {
//             curr[j] = j;
//         }
//         for (int i = 1; i <= m; i++) {
//             prev = curr[0];
//             curr[0] = i;
//             for (int j = 1; j <= n; j++) {
//                 int temp = curr[j];
//                 if (word1[i - 1] == word2[j - 1]) {
//                     curr[j] = prev;
//                 } else {
//                     curr[j] = min(prev, min(curr[j - 1], curr[j])) + 1;
//                 }
//                 prev = temp;
//             }
//         }
//         return curr[n];
//     }
// };
```
