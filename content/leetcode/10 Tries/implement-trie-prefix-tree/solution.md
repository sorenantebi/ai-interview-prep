---
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/implement-trie-prefix-tree/
neetcode: https://neetcode.io/problems/implement-prefix-tree
---
# Implement Trie Prefix Tree - Solution

**Question:** Implement Trie Prefix Tree - Question · **Difficulty:** Medium

## Intuition

Each trie node represents a prefix and maps a character to the child node for that extended prefix. Words sharing a prefix share the path, so every operation walks at most one node per character. An `end` flag on a node distinguishes "a complete inserted word ends here" from "this is merely a prefix".

## Approach

1. A `TrieNode` holds `children: dict[str, TrieNode]` and `end: bool`.
2. `insert`: walk from the root, creating missing children; mark the last node `end = True`.
3. A helper `_find(s)` walks the path for `s` and returns the final node, or `None` if a character is missing.
4. `search(word)`: `_find(word)` exists **and** has `end = True`. `startsWith(prefix)`: `_find(prefix)` exists.

## Code

```python
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.end = False


class Trie:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        curr = self.root
        for c in word:
            i = ord(c) - ord("a")
            if curr.children[i] is None:
                curr.children[i] = TrieNode()
            curr = curr.children[i]
        curr.end = True

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        curr = self.root
        for c in word:
            i = ord(c) - ord("a")
            if curr.children[i] is None:
                return False
            curr = curr.children[i]
        return curr.end

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        curr = self.root
        for c in prefix:
            i = ord(c) - ord("a")
            if curr.children[i] is None:
                return False
            curr = curr.children[i]
        return True
```

## Complexity

- **Time:** `O(L)` per operation, where `L` is the length of the word/prefix.
- **Space:** `O(total characters inserted)` — at most one node per inserted character.

## Other Approaches

- **Fixed array of 26 children per node:** same complexity, faster constant factor but more memory per node — Time `O(L)`, Space `O(26 · nodes)`.
- **Hash set of words + hash set of all prefixes:** `O(L)` lookups but insertion costs `O(L^2)` time and space for storing every prefix.

## Key Takeaway

A trie is a tree of dicts keyed by character with an end-of-word flag; it is the go-to structure whenever many lookups share prefixes (autocomplete, word search, wildcard matching).
