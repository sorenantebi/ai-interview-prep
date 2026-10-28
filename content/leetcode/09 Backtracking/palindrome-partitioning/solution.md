---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/palindrome-partitioning/
neetcode: https://neetcode.io/problems/palindrome-partitioning
---
# Palindrome Partitioning - Solution

**Question:** Palindrome Partitioning - Question · **Difficulty:** Medium

## Intuition

Choose the first piece, then recursively partition the rest: from position `start`, try every end index `end` such that `s[start:end+1]` is a palindrome, add it to the path, and recurse from `end + 1`. Precomputing a palindrome table with DP makes each check `O(1)`.

## Approach

1. Build `pal[i][j]` = whether `s[i..j]` is a palindrome: `s[i] == s[j]` and (`j - i < 2` or `pal[i+1][j-1]`), filling `i` from the end.
2. `dfs(start)`: if `start == n`, record a copy of `path`.
3. For each `end` from `start` to `n - 1` with `pal[start][end]`: append `s[start:end+1]`, recurse with `dfs(end + 1)`, pop.

## Code

```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        res, part = [], []

        def dfs(i):
            if i >= len(s):
                res.append(part.copy())
                return
            for j in range(i, len(s)):
                if self.isPali(s, i, j):
                    part.append(s[i : j + 1])
                    dfs(j + 1)
                    part.pop()

        dfs(0)
        return res

    def isPali(self, s, l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l, r = l + 1, r - 1
        return True
```

## Complexity

- **Time:** `O(n * 2^n)` — up to `2^(n-1)` partitions, each copied/built in `O(n)`; the DP table is `O(n^2)`.
- **Space:** `O(n^2)` for the palindrome table plus `O(n)` recursion (output excluded).

## Other Approaches

- **Check palindromes on the fly:** test `sub == sub[::-1]` inside the DFS instead of a table — Time `O(n^2 * 2^n)` worst case, Space `O(n)`.

## Key Takeaway

"All ways to split a string" = backtracking over the end of the first piece; precompute validity of substrings (here palindromes) so each branch check is `O(1)`.

## C++

```cpp
/*
    Given a string, partition such that every substring is a palindrome, return all possible ones
    Ex. s = "aab" -> [["a","a","b"],["aa","b"]], s = "a" -> [["a"]]

    Generate all possible substrings at idx, if palindrome potential candidate, backtrack after

    Time: O(n x 2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<string>> partition(string s) {
        vector<string> curr;
        vector<vector<string>> result;
        dfs(s, 0, curr, result);
        return result;
    }
private:
    void dfs(string s, int start, vector<string>& curr, vector<vector<string>>& result) {
        if (start == s.size()) {
            result.push_back(curr);
            return;
        }
        for (int i = start; i < s.size(); i++) {
            if (isPalindrome(s, start, i)) {
                string str = s.substr(start, i - start + 1);
                curr.push_back(str);
                dfs(s, i + 1, curr, result);
                curr.pop_back();
            }
        }
    }
    bool isPalindrome(string s, int left, int right) {
        while (left < right) {
            if (s[left] != s[right]) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
};
```
