---
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/design-add-and-search-words-data-structure/
neetcode: https://neetcode.io/problems/design-word-search-data-structure
---
# Design Add And Search Words Data Structure

**Topic:** Tries · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/design-add-and-search-words-data-structure/) · [NeetCode](https://neetcode.io/problems/design-word-search-data-structure)

## Problem

Design a data structure that stores words and supports searching with wildcards. Implement `WordDictionary`:

- `WordDictionary()` — create an empty structure.
- `addWord(word)` — store `word`.
- `search(word)` — return `True` if some stored word matches `word`, else `False`. The query may contain `'.'` characters, each of which matches **any single** letter. A match must have exactly the same length.

## Examples

**Example 1**
```text
Input:  ["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
        [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
Output: [null,null,null,null,false,true,true,true]
```

**Example 2**
```text
Input:  ["WordDictionary","addWord","search","search"]
        [[],["a"],["."],[".."]]
Output: [null,null,true,false]
```

## Constraints

- `1 <= word.length <= 25`
- Words passed to `addWord` contain only lowercase English letters
- Queries passed to `search` contain lowercase letters or `'.'`
- Each query contains at most `2` dots
- At most `10^4` calls in total
