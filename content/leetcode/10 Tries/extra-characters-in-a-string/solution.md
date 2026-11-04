---
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/extra-characters-in-a-string/
neetcode: https://neetcode.io/problems/extra-characters-in-a-string
---
# Extra Characters in a String - Solution

## Intuition

At each position we either skip the character (it becomes extra) or match a dictionary word starting there and jump past it. This is a classic prefix DP over the string. A trie lets us enumerate all dictionary words starting at a position in a single walk, stopping as soon as no word shares the current prefix.

## Approach

1. Build a trie from all words in `dictionary`, marking nodes where a word ends.
2. Let `dp[i]` be the minimum number of extra characters in the suffix `s[i:]`, with `dp[n] = 0`.
3. Iterate `i` from `n - 1` down to `0`.
4. Start with `dp[i] = dp[i + 1] + 1`, which treats `s[i]` as extra.
5. Walk the trie from the root along `s[i], s[i+1], ...`. Stop when there is no child for the next character.
6. Whenever the current node ends a word at index `j`, update `dp[i] = min(dp[i], dp[j + 1])`.
7. Return `dp[0]`.

## Code

```python
from typing import List, Optional

class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        root = {}
        for word in dictionary:
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node["$"] = True  # end-of-word marker

        n = len(s)
        dp = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            dp[i] = dp[i + 1] + 1
            node = root
            for j in range(i, n):
                node = node.get(s[j])
                if node is None:
                    break
                if "$" in node:
                    dp[i] = min(dp[i], dp[j + 1])
        return dp[0]
```

## Complexity

- **Time:** `O(n^2 + L)` — for each of the `n` start positions the trie walk covers at most `n` characters; building the trie costs `O(L)` where `L` is the total length of all words.
- **Space:** `O(L + n)` — the trie holds at most `L` nodes and the DP array has `n + 1` entries.

## Other Approaches

- **Top-down memoization with a set:** recurse on the start index, try every substring `s[i:j]` found in a hash set of words, and cache results — Time `O(n^3)` / Space `O(n + L)`
- **Bottom-up DP with a set:** same recurrence as above, iterated over indices, checking each substring against a hash set — Time `O(n^3)` / Space `O(n + L)`

## C++

```cpp
/*
  You are given a 0-indexed string s and a dictionary of words dictionary. 
  You have to break s into one or more non-overlapping substrings such that each substring is present in dictionary. 
  There may be some extra characters in s which are not present in any of the substrings.

  Return the minimum number of extra characters left over if you break up s optimally.

  Ex. Input: s = "leetscode", dictionary = ["leet","code","leetcode"]
      Output: 1
      Explanation: We can break s in two substrings: "leet" from index 0 to 3 and "code" from index 5 to 8. There is only 1 unused character (at index 4), so we return 1.

  Time  : O(N^M)    M = dictionary.size(), N = s.size()
  Space : O(N)
*/

class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        int n = s.size();
        vector<int> dp(n + 1, n);

        dp[0] = 0; 

        for (int i = 1; i <= n; ++i) {
            for(int j = 0 ; j < dictionary.size() ; ++j) {
                int len = dictionary[j].size();
                if (i >= len && s.substr(i - len, len) == dictionary[j]) {
                    dp[i] = min(dp[i], dp[i - len]);
                }
            }
            dp[i] = min(dp[i], dp[i - 1] + 1);
        }

        return dp[n];
    }
};
```
