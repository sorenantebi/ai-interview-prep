---
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/implement-trie-prefix-tree/
neetcode: https://neetcode.io/problems/implement-prefix-tree
---
# Implement Trie Prefix Tree

**Topic:** Tries · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/implement-trie-prefix-tree/) · [NeetCode](https://neetcode.io/problems/implement-prefix-tree)

## Problem

A trie (prefix tree) stores a set of strings so that words and prefixes can be looked up efficiently. Implement the class `Trie`:

- `Trie()` — create an empty trie.
- `insert(word)` — add `word` to the trie.
- `search(word)` — return `True` if `word` was previously inserted (as a complete word), else `False`.
- `startsWith(prefix)` — return `True` if any previously inserted word begins with `prefix`, else `False`.

## Examples

**Example 1**
```text
Input:  ["Trie","insert","search","search","startsWith","insert","search"]
        [[],["apple"],["apple"],["app"],["app"],["app"],["app"]]
Output: [null,null,true,false,true,null,true]
```

**Example 2**
```text
Input:  ["Trie","insert","startsWith","search"]
        [[],["a"],["b"],["a"]]
Output: [null,null,false,true]
```

## Constraints

- `1 <= word.length, prefix.length <= 2000`
- `word` and `prefix` consist only of lowercase English letters
- At most `3 * 10^4` calls in total
