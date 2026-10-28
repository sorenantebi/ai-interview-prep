---
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/design-add-and-search-words-data-structure/
neetcode: https://neetcode.io/problems/design-word-search-data-structure
---
# Design Add And Search Words Data Structure - Solution

**Question:** Design Add And Search Words Data Structure - Question · **Difficulty:** Medium

## Intuition

Store words in a trie. A normal letter follows a single child, but a `'.'` must try every child at that position, so search becomes a DFS over the trie. Since queries contain at most two dots, branching stays small in practice.

## Approach

1. `addWord`: standard trie insertion, marking the last node as a word end.
2. `search`: run `dfs(i, node)` meaning "can `word[i:]` be matched starting at `node`?".
3. If `i == len(word)`, return `node.end`.
4. If `word[i] == '.'`, return `True` if `dfs(i + 1, child)` succeeds for any child; otherwise follow the matching child (return `False` if missing).

## Code

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # a : TrieNode
        self.word = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]
        cur.word = True

    def search(self, word: str) -> bool:
        def dfs(j, root):
            cur = root

            for i in range(j, len(word)):
                c = word[i]
                if c == ".":
                    for child in cur.children.values():
                        if dfs(i + 1, child):
                            return True
                    return False
                else:
                    if c not in cur.children:
                        return False
                    cur = cur.children[c]
            return cur.word

        return dfs(0, self.root)
```

## Complexity

- **Time:** `addWord` is `O(L)`. `search` is `O(L)` without dots and `O(26^d · L)` worst case with `d` dots (`d <= 2` here).
- **Space:** `O(total characters added)` for the trie; `O(L)` recursion stack for search.

## Other Approaches

- **Bucket words by length, then compare each candidate character by character:** Time `O(n · L)` per search, Space `O(total characters)`.
- **Regex over a set of words:** simple but `O(n · L)` per query.

## Key Takeaway

Wildcards on a trie turn lookup into DFS/backtracking: deterministic characters follow one edge, wildcards fan out over all children.

## C++

```cpp
/*
    Design add & search words data structure

    Implement trie, handle wildcards: traverse all children & search substrings

    Time: O(m x 26^n) -> m = # of words, n = length of words
    Space: O(n)
*/

class TrieNode {
public:
    TrieNode* children[26];
    bool isWord;
    
    TrieNode() {
        for (int i = 0; i < 26; i++) {
            children[i] = NULL;
        }
        isWord = false;
    }
};

class WordDictionary {
public:
    WordDictionary() {
        root = new TrieNode();
    }
    
    void addWord(string word) {
        TrieNode* node = root;
        int curr = 0;
        
        for (int i = 0; i < word.size(); i++) {
            curr = word[i] - 'a';
            if (node->children[curr] == NULL) {
                node->children[curr] = new TrieNode();
            }
            node = node->children[curr];
        }
        
        node->isWord = true;
    }
    
    bool search(string word) {
        TrieNode* node = root;
        return searchInNode(word, 0, node);
    }
private:
    TrieNode* root;
    
    bool searchInNode(string& word, int i, TrieNode* node) {
        if (node == NULL) {
            return false;
        }
        if (i == word.size()) {
            return node->isWord;
        }
        if (word[i] != '.') {
            return searchInNode(word, i + 1, node->children[word[i] - 'a']);
        }
        for (int j = 0; j < 26; j++) {
            if (searchInNode(word, i + 1, node->children[j])) {
                return true;
            }
        }
        return false;
    }
};

/**
 * Your WordDictionary object will be instantiated and called as such:
 * WordDictionary* obj = new WordDictionary();
 * obj->addWord(word);
 * bool param_2 = obj->search(word);
 */
```
