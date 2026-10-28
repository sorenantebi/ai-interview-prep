---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/alien-dictionary/
neetcode: https://neetcode.io/problems/foreign-dictionary
---
# Alien Dictionary - Solution

**Question:** Alien Dictionary - Question · **Difficulty:** Hard

## Intuition

Each adjacent pair of words gives at most one ordering fact: at the first differing position, the letter in the first word precedes the letter in the second. These facts form a directed graph over letters, and any **topological order** of it is a valid alphabet. A cycle — or a longer word placed before its own prefix — makes the input invalid.

## Approach

1. Create a node (with in-degree 0) for every letter that appears.
2. For each adjacent pair `(w1, w2)`: if `w1` is longer and `w2` is a prefix of it, return `""`. Otherwise find the first differing letters `a != b` and add edge `a -> b` (once).
3. Run Kahn's algorithm: start with in-degree-0 letters, pop, append to the result, and decrement neighbours' in-degrees.
4. If the result doesn't contain every letter, there was a cycle: return `""`.

## Code

```python
class Solution:
    def alienOrder(self, words: List[str]) -> str:
        adj = {char: set() for word in words for char in word}

        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            minLen = min(len(w1), len(w2))
            if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:
                return ""
            for j in range(minLen):
                if w1[j] != w2[j]:
                    print(w1[j], w2[j])
                    adj[w1[j]].add(w2[j])
                    break

        visited = {}  # {char: bool} False visited, True current path
        res = []

        def dfs(char):
            if char in visited:
                return visited[char]

            visited[char] = True

            for neighChar in adj[char]:
                if dfs(neighChar):
                    return True

            visited[char] = False
            res.append(char)

        for char in adj:
            if dfs(char):
                return ""

        res.reverse()
        return "".join(res)
```

## Complexity

- **Time:** `O(C)` — `C` is the total number of characters across all words (building edges), plus `O(U + E)` for the topological sort with `U <= 26` letters.
- **Space:** `O(U + E)` — at most `26` nodes and `26^2` edges, i.e. `O(1)` relative to input size.

## Other Approaches

- **DFS topological sort with 3-colour cycle detection:** post-order DFS, reverse at the end, return `""` on a back edge — Time `O(C)`, Space `O(U + E)`.

## Key Takeaway

Turn "sorted list under an unknown order" into pairwise precedence edges (only the first difference matters), then topologically sort; remember the prefix edge case.

## C++

```cpp
#include<iostream>
#include<map>
#include<vector>
#include<queue>
using namespace std;

class Solution {
public:
    string alienOrder(vector<string>& words) {
        map<char,int> degree;
        map<char, vector<char>> graph;
        int n = words.size();

        for (auto& word : words) {
            for (auto& ch : word) {
                degree[ch] = 0;
        }

        for (int i = 0; i < n - 1; i++) {
         int l = min((int)words[i].size(), (int)words[i + 1].size());
         for (int j = 0; j < l; j++) {
            char x = words[i][j];
            char y = words[i + 1][j];
            if (x != y) {
               graph[x].push_back(y);
               degree[y]++;
               break;
            }
         }
      }
      
      string ret = "";
      queue<char> q;
      map<char, int>::iterator it = degree.begin();
      while (it != degree.end()) {
         if (it->second == 0) {
            q.push(it->first);
         }
         it++;
      }

      while (!q.empty()) {
         char x = q.front();
         q.pop();
         ret += x;
         vector<char>::iterator sit = graph[x].begin();
         while (sit != graph[x].end()) {
            degree[*sit]--;
            if (degree[*sit] == 0) {
               q.push(*sit);
            }
            sit++;
         }
      }
      return ret.size() == degree.size() ? ret : "";
      }
    }
};
```
