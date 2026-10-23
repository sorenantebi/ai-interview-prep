---
topic: "Tries"
difficulty: Hard
leetcode: https://leetcode.com/problems/word-search-ii/
neetcode: https://neetcode.io/problems/search-for-word-ii
---
# Word Search II - Solution

**Question:** Word Search II - Question · **Difficulty:** Hard

## Intuition

Running a separate Word Search for each word repeats the same board exploration over and over. Instead, put all words in a trie and run one backtracking DFS from every cell, walking the trie in lockstep with the board path. A path is abandoned as soon as it is not a prefix of any word, and each trie node that ends a word stores that word so it can be reported directly.

## Approach

1. Build a trie; at the node where a word ends, store `node["$"] = word`.
2. For each cell, start `dfs(r, c, parent_node)` if the cell's letter is a child of the root.
3. In `dfs`: move to the child node for `board[r][c]`. If it contains `"$"`, add the word to the result and delete the marker (avoids duplicates).
4. Mark the cell as visited (temporarily set it to `"#"`), recurse into the 4 neighbours whose letters are children of the current node, then restore the cell.
5. Pruning: if the child node becomes empty after exploring, remove it from its parent so exhausted branches are never re-explored.

## Code

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.isWord = False
        self.refs = 0

    def addWord(self, word):
        cur = self
        cur.refs += 1
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]
            cur.refs += 1
        cur.isWord = True

    def removeWord(self, word):
        cur = self
        cur.refs -= 1
        for c in word:
            if c in cur.children:
                cur = cur.children[c]
                cur.refs -= 1


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for w in words:
            root.addWord(w)

        ROWS, COLS = len(board), len(board[0])
        res, visit = set(), set()

        def dfs(r, c, node, word):
            if (
                r not in range(ROWS) 
                or c not in range(COLS)
                or board[r][c] not in node.children
                or node.children[board[r][c]].refs < 1
                or (r, c) in visit
            ):
                return

            visit.add((r, c))
            node = node.children[board[r][c]]
            word += board[r][c]
            if node.isWord:
                node.isWord = False
                res.add(word)
                root.removeWord(word)

            dfs(r + 1, c, node, word)
            dfs(r - 1, c, node, word)
            dfs(r, c + 1, node, word)
            dfs(r, c - 1, node, word)
            visit.remove((r, c))

        for r in range(ROWS):
            for c in range(COLS):
                dfs(r, c, root, "")

        return list(res)
```

## Complexity

- **Time:** `O(m · n · 3^(L-1))` worst case, where `L` is the max word length (4 directions at the first step, then at most 3 since we can't go back) — plus `O(total word length)` to build the trie. Pruning makes it much faster in practice.
- **Space:** `O(total word length)` for the trie; `O(L)` recursion stack.

## Other Approaches

- **Word Search per word:** run a backtracking search for each word separately — Time `O(W · m · n · 3^L)`, Space `O(L)`; too slow for `3 * 10^4` words.

## Key Takeaway

When searching for many words at once, build a trie and walk it during the DFS; store the word at its terminal node and prune emptied branches to avoid redundant work.
