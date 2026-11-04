---
topic: "Heap - Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/reorganize-string/
neetcode: https://neetcode.io/problems/reorganize-string
---
# Reorganize String - Solution

## Intuition

A valid arrangement exists only if the most frequent character occupies at most `ceil(n / 2)` positions, i.e. `max_count <= (n + 1) // 2`. Greedily placing the character with the highest remaining count (that isn't the one just placed) keeps the most frequent characters spread out, which is exactly what a max-heap gives us.

## Approach

1. Count the frequency of each character.
2. Push `(-count, char)` for each character into a max-heap (via negated counts).
3. Repeatedly pop the most frequent character and append it to the result. Hold it back as `prev` rather than pushing it right away, so it cannot be placed twice in a row.
4. After placing a character, push the previously held-back character back into the heap if it still has remaining count. Then hold the current one (with its decremented count).
5. If the heap is empty while a held-back character still has count left, no valid arrangement exists, so return `""`.
6. Otherwise return the joined result.

## Code

```python
class Solution:
    def reorganizeString(self, s: str) -> str:
        count = Counter(s)  # Hashmap, count each char
        maxHeap = [[-cnt, char] for char, cnt in count.items()]
        heapq.heapify(maxHeap)  # O(n)

        prev = None
        res = ""
        while maxHeap or prev:
            if prev and not maxHeap:
                return ""
            # most frequent, except prev
            cnt, char = heapq.heappop(maxHeap)
            res += char
            cnt += 1

            if prev:
                heapq.heappush(maxHeap, prev)
                prev = None
            if cnt != 0:
                prev = [cnt, char]
        return res
```

## Complexity

- **Time:** `O(n log k)` — each of the `n` characters is pushed and popped once from a heap of at most `k = 26` distinct characters, so effectively `O(n)`.
- **Space:** `O(k)` — the heap and counter hold at most 26 entries (plus `O(n)` for the output).

## Other Approaches

- **Greedy with even/odd slot filling:** sort characters by frequency, fill even indices first then odd indices with the most frequent character first; return `""` if the max count exceeds `(n + 1) // 2` — Time `O(n + k log k)` / Space `O(n)`
- **Counting without a heap:** at each step pick the character with the largest remaining count different from the last placed by scanning all 26 letters — Time `O(26 · n)` / Space `O(k)`

## C++

```cpp
// Time: O(NlogN)
// Space: O(N)

class Solution {
public:
    string reorganizeString(string s) {
        string res="";

        unordered_map<char, int> mp;
        priority_queue<pair<int, char>> maxh;
        
        for(auto ch : s)
            mp[ch] += 1;
        
        for(auto m : mp)
            maxh.push(make_pair(m.second, m.first));
        
        while(maxh.size() > 1){
            auto top1= maxh.top();
            maxh.pop();
            auto top2 = maxh.top();
            maxh.pop();
            
            res += top1.second;
            res += top2.second;
            
            if(--top1.first > 0)
                maxh.push(top1);
            
            if(--top2.first > 0)
                maxh.push(top2);
        }
        
        if(!maxh.empty()){
            if(maxh.top().first > 1)
                return "";
            
            else
                res += maxh.top().second;
        }
        
        return res;
    }
};
```
