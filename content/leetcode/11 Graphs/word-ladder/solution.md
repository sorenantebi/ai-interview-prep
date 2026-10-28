---
topic: "Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/word-ladder/
neetcode: https://neetcode.io/problems/word-ladder
---
# Word Ladder - Solution

**Question:** Word Ladder - Question · **Difficulty:** Hard

## Intuition

Words are nodes; two words are connected if they differ by exactly one letter. The shortest transformation sequence is a shortest path in an unweighted graph, so use **BFS**. Rather than comparing every pair of words, generate neighbors by trying all 26 letters at each position and keeping only candidates that are in the (unvisited) dictionary.

## Approach

1. Put `wordList` in a set; if `endWord` is missing, return `0`.
2. BFS from `beginWord` with level counter starting at 1.
3. For each word in the current level, for each position and each letter `a`–`z`, form a candidate; if it is `endWord`, return `level + 1`; if it is in the remaining word set, remove it (mark visited) and enqueue it.
4. If BFS ends, return `0`.

## Code

```python
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        nei = collections.defaultdict(list)
        wordList.append(beginWord)
        for word in wordList:
            for j in range(len(word)):
                pattern = word[:j] + "*" + word[j + 1 :]
                nei[pattern].append(word)

        visit = set([beginWord])
        q = deque([beginWord])
        res = 1
        while q:
            for i in range(len(q)):
                word = q.popleft()
                if word == endWord:
                    return res
                for j in range(len(word)):
                    pattern = word[:j] + "*" + word[j + 1 :]
                    for neiWord in nei[pattern]:
                        if neiWord not in visit:
                            visit.add(neiWord)
                            q.append(neiWord)
            res += 1
        return 0
```

## Complexity

- **Time:** `O(N * L^2 * 26)` — `N` words, each visited once; `L * 26` candidates per word, each costing `O(L)` to build and hash.
- **Space:** `O(N * L)` — the word set and BFS queue.

## Other Approaches

- **Wildcard pattern buckets:** map patterns like `h*t` to the words matching them and BFS through buckets — Time `O(N * L^2)`, Space `O(N * L^2)`.
- **Bidirectional BFS:** expand from both ends, always growing the smaller frontier — same worst case, much faster in practice.

## Key Takeaway

Shortest number of single-step edits = BFS over an implicit graph; generate neighbors on the fly and delete visited words from the dictionary set.

## C++

```cpp
/*
    Given 2 words & a dictionary, return min # of words to transform b/w them
    Ex. begin = "hit", end = "cog", dict = ["hot","dot","dog","lot","log","cog"] -> 5
    "hit" -> "hot" -> "dot" -> "dog" -> "cog"

    BFS, change 1 letter at a time (neighbors), if in dict add to queue, else skip

    Time: O(m^2 x n) -> m = length of each word, n = # of words in input word list
    Space: O(m^2 x n)
*/

class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> dict;
        for (int i = 0; i < wordList.size(); i++) {
            dict.insert(wordList[i]);
        }
        
        queue<string> q;
        q.push(beginWord);
        
        int result = 1;
        
        while (!q.empty()) {
            int count = q.size();
            
            for (int i = 0; i < count; i++) {
                string word = q.front();
                q.pop();
                
                if (word == endWord) {
                    return result;
                }
                dict.erase(word);
                
                for (int j = 0; j < word.size(); j++) {
                    char c = word[j];
                    for (int k = 0; k < 26; k++) {
                        word[j] = k + 'a';
                        if (dict.find(word) != dict.end()) {
                            q.push(word);
                            dict.erase(word);
                        }
                        word[j] = c;
                    }
                }
            }
            
            result++;
        }
        
        return 0;
    }
};
```
