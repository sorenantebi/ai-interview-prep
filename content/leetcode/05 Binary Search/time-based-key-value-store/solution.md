---
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/time-based-key-value-store/
neetcode: https://neetcode.io/problems/time-based-key-value-store
---
# Time Based Key Value Store - Solution

**Question:** Time Based Key Value Store - Question · **Difficulty:** Medium

## Intuition

Because `set` timestamps arrive in increasing order, each key's list of `(timestamp, value)` pairs is already sorted. A `get` asks for the last entry with timestamp `<= t`, which is a classic upper-bound binary search on that list.

## Approach

1. Keep a dict `key -> list of (timestamp, value)`; `set` simply appends.
2. `get(key, t)`: binary search the key's list for the rightmost timestamp `<= t`.
3. Track the best candidate while searching: when `times[mid] <= t`, record it and move right; otherwise move left.
4. Return the recorded value, or `""` if none was found.

## Code

```python
class TimeMap:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.keyStore = {}  # key : list of [val, timestamp]

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.keyStore:
            self.keyStore[key] = []
        self.keyStore[key].append([value, timestamp])

    def get(self, key: str, timestamp: int) -> str:
        res, values = "", self.keyStore.get(key, [])
        l, r = 0, len(values) - 1
        while l <= r:
            m = (l + r) // 2
            if values[m][1] <= timestamp:
                res = values[m][0]
                l = m + 1
            else:
                r = m - 1
        return res
```

## Complexity

- **Time:** `O(1)` for `set`, `O(log k)` for `get` where `k` is the number of entries for that key.
- **Space:** `O(n)` — all stored entries.

## Other Approaches

- **Linear scan backwards on `get`:** walk the key's list from the end until a timestamp `<= t` — `get` is `O(k)`, Space `O(n)`.
- **`bisect.bisect_right`:** keep a parallel list of timestamps and use `bisect_right(times, t) - 1` — same `O(log k)`, less code.

## Key Takeaway

Append-only, time-ordered data is naturally sorted — answer "latest value at or before t" with an upper-bound binary search.

## C++

```cpp
/*
    Design time-based key-value structure, multiple vals at diff times

    Hash map, since timestamps are naturally in order, binary search

    Time: O(log n)
    Space: O(n)
*/

class TimeMap {
public:
    TimeMap() {
        
    }
    
    void set(string key, string value, int timestamp) {
        m[key].push_back({timestamp, value});
    }
    
    string get(string key, int timestamp) {
        if (m.find(key) == m.end()) {
            return "";
        }
        
        int low = 0;
        int high = m[key].size() - 1;
        
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (m[key][mid].first < timestamp) {
                low = mid + 1;
            } else if (m[key][mid].first > timestamp) {
                high = mid - 1;
            } else {
                return m[key][mid].second;
            }
        }
        
        if (high >= 0) {
            return m[key][high].second;
        }
        return "";
    }
private:
    unordered_map<string, vector<pair<int, string>>> m;
};

/**
 * Your TimeMap object will be instantiated and called as such:
 * TimeMap* obj = new TimeMap();
 * obj->set(key,value,timestamp);
 * string param_2 = obj->get(key,timestamp);
 */
```
