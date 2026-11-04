---
topic: "Backtracking"
difficulty: Hard
leetcode: https://leetcode.com/problems/word-break-ii/
neetcode: https://neetcode.io/problems/word-break-ii
---
# Word Break II - Solution

## Intuition

Every sentence is a first word followed by a sentence for the remaining suffix. The set of sentences for a given suffix never changes, so computing it once per start index (memoization) avoids repeated work. Empty results are cached too, which prunes dead ends such as in Example 3.

## Approach

1. Put `wordDict` in a set and record the maximum word length.
2. Define `dfs(start)` that returns all sentences for `s[start:]`.
3. If `start == len(s)`, return `[""]`, representing one empty sentence.
4. For each `end` from `start + 1` to `min(len(s), start + max_len)`, check whether `s[start:end]` is in the set.
5. If it is, join the word with every sentence returned by `dfs(end)`, adding a space only when the remainder is non-empty.
6. Cache the result per `start` and return `dfs(0)`.

## Code

```python
from typing import List, Optional

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)
        max_len = max(len(w) for w in wordDict)
        n = len(s)
        memo = {}

        def dfs(start: int) -> List[str]:
            if start == n:
                return [""]
            if start in memo:
                return memo[start]
            res = []
            for end in range(start + 1, min(n, start + max_len) + 1):
                word = s[start:end]
                if word in words:
                    for rest in dfs(end):
                        res.append(word + " " + rest if rest else word)
            memo[start] = res
            return res

        return dfs(0)
```

## Complexity

- **Time:** `O(n * L + K)` where `L` is the max word length and `K` is the total size of all generated sentences (bounded by `10^5`) — each start index is solved once, and the work is dominated by building the output strings (substring checks cost up to `O(L)` each). In the worst case the sentence count is exponential in `n`.
- **Space:** `O(n + K)` — the memo table holds the sentences for each suffix, plus the recursion depth of `O(n)`.

## Other Approaches

- **Plain backtracking (no memo):** Try every prefix and recurse, building the sentence in a path list — Time `O(2^n * n)` / Space `O(n)` excluding output.
- **Word Break I pre-check + backtracking:** Run a boolean DP for feasibility first, and return `[]` immediately if no segmentation exists — Time `O(n^2)` for the check plus output cost / Space `O(n)`.
- **Bottom-up DP:** Build `dp[i]` as the list of sentences for the prefix `s[:i]` — Time `O(n * L + K)` / Space `O(K)`.
- **Trie of the dictionary:** Walk a trie from each start index to find matching words without slicing — Time `O(n * L + K)` / Space `O(total dictionary characters)`.
