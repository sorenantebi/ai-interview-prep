---
topic: "Graphs"
difficulty: Easy
leetcode: https://leetcode.com/problems/verifying-an-alien-dictionary/
neetcode: https://neetcode.io/problems/verifying-an-alien-dictionary
---
# Verifying an Alien Dictionary - Solution

## Intuition

A list is sorted if and only if every adjacent pair of words is in order. Comparing two words only requires finding the first position where they differ and checking which letter comes first in the alien alphabet. If no position differs, the shorter word must come first.

## Approach

1. Build a map from each letter to its index in `order`.
2. For each adjacent pair `(a, b)` in `words`, scan the characters side by side.
3. At the first index where the letters differ, if `a`'s letter has a larger rank than `b`'s, return `False`; otherwise this pair is fine, so stop scanning it.
4. If no differing character is found, `a` is a prefix of `b` or equal to it, so the pair is valid only when `len(a) <= len(b)`.
5. If every pair passes, return `True`.

## Code

```python
class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        # first differing char
        # if word A is prefix of word B, word B must be AFTER word A
        orderInd = { c : i for i, c in enumerate(order)}
        
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            
            for j in range(len(w1)):
                if j == len(w2):
                    return False
                
                if w1[j] != w2[j]:
                    if orderInd[w2[j]] < orderInd[w1[j]]:
                        return False
                    break
        return True
```

## Complexity

- **Time:** `O(N)` — where `N` is the total number of characters across all words; each adjacent pair is scanned at most once up to the shorter word's length.
- **Space:** `O(1)` — the rank map always holds 26 entries.

## Other Approaches

- **Transform and sort-compare:** map each word to a tuple of ranks and check that the list equals its sorted version — Time `O(N + W log W · L)` / Space `O(N)`
- **Topological sort view:** the problem is the verification side of "Alien Dictionary", where adjacent-word comparisons yield graph edges; here the order is given, so a direct comparison suffices — Time `O(N)` / Space `O(1)`

## C++

```cpp
/*
    Given list of words in another language, return string such that:
    Letters are sorted in lexicographical incr order wrt this language
    Ex. words = ["wrt","wrf","er","ett","rftt"]

    Build graph + record edges, BFS + topological sort, check cyclic

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    string alienOrder(vector<string> &words) {
        
        unordered_map<char, unordered_set<char>> graph;
        unordered_map<char, int> indegree;

        // indegree make all char 0
        for(auto word : words){
            for(auto c : word){
                indegree[c]=0;
            }
        }

        for(int i=0; i<words.size()-1; i++){
            string curr = words[i];
            string next = words[i+1];
            
            bool flag = false;
            int len = min(curr.length(), next.length());
            for(int j=0; j<len; j++){
                char ch1 = curr[j];
                char ch2 = next[j];

                if(ch1 != ch2){
                    unordered_set<char> set;

                    if(graph.find(ch1) != graph.end()){
                        set = graph[ch1];

                        if(set.find(ch2) == set.end()){
                            set.insert(ch2);
                            indegree[ch2]++;
                            graph[ch1] = set;
                        }
                    }
                    else{
                        set.insert(ch2);
                        indegree[ch2]++;
                        graph[ch1] = set;
                    }

                    flag = true;
                    break;
                }
                
            }

            if(flag == false and (curr.length() > next.length())) return "";
        }

        priority_queue<char, vector<char>, greater<char>> q;

        for(auto it : indegree){
            if(it.second == 0){
                //cout<<it.first<<endl;
                q.push(it.first);
            }
        }

        int count=0;
        string ans = "";

        while(q.size()>0){
            auto rem = q.top();
            q.pop();

            ans += rem;
            count++;

            if(graph.find(rem) != graph.end()){
                unordered_set<char> nbrs = graph[rem];

                for(auto nbr : nbrs){
                    indegree[nbr]--;
                    if(indegree[nbr] == 0){
                        q.push(nbr);
                    }
                }
            }
        }

        if(count == indegree.size()){
            return ans;
        }
        return "";
    }
};
```
