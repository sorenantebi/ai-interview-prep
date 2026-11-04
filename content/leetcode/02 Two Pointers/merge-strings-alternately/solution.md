---
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/merge-strings-alternately/
neetcode: https://neetcode.io/problems/merge-strings-alternately
---
# Merge Strings Alternately - Solution

## Intuition

Walk both strings together with a shared index, taking one character from each in turn. Once the shorter string runs out, whatever is left of the longer one goes on the end unchanged.

## Approach

1. Create an empty list `res` to collect characters.
2. Loop `i` from `0` to `min(len(word1), len(word2)) - 1`, appending `word1[i]` then `word2[i]`.
3. After the loop, append the leftover suffix of each string (`word1[n:]` and `word2[n:]`, where `n` is the shorter length); at most one is non-empty.
4. Join the list into a single string and return it.

## Code

```python
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        i = j = 0
        res = []

        while i < len(word1) and j < len(word2):
            res.append(word1[i])
            res.append(word2[j])
            i += 1
            j += 1
        res.append(word1[i:])
        res.append(word2[j:])
        return ''.join(res)
```

## Complexity

- **Time:** `O(m + n)` — every character of both strings is visited once.
- **Space:** `O(m + n)` — the output string holds all characters.

## Other Approaches

- **Two explicit pointers:** advance `i` and `j` in a `while i < m or j < n` loop, appending from each string when in range — Time `O(m + n)` / Space `O(m + n)`
- **`itertools.zip_longest`:** zip both strings with `fillvalue=""` and join the pairs — Time `O(m + n)` / Space `O(m + n)`

## C++

```cpp
class Solution {
public:
    string mergeAlternately(string word1, string word2)
    {
        int i=0;
        string final="";

        while(i < word1.size() && i < word2.size())
            final = final + word1[i] + word2[i++];

        while(i < word1.size())
            final += word1[i++];
        while(i < word2.size())
            final += word2[i++];

        return final;
    }
};
```
