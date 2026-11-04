---
topic: "Stack"
difficulty: Hard
leetcode: https://leetcode.com/problems/maximum-frequency-stack/
neetcode: https://neetcode.io/problems/maximum-frequency-stack
---
# Maximum Frequency Stack - Solution

## Intuition

Think of each value as being placed on "layers". The first time a value is pushed it goes on layer 1, the second time on layer 2, and so on. The most frequent element is always on the highest non-empty layer, and within that layer the most recently pushed element is on top. So popping means taking the top of the highest layer.

## Approach

1. Keep `freq[val]`, the current count of each value.
2. Keep `groups[f]`, a stack of the values that reached frequency `f`, in push order.
3. Track `max_freq`, the highest non-empty layer.
4. `push(val)`: increment `freq[val]`, append `val` to `groups[freq[val]]`, and update `max_freq`.
5. `pop()`: pop from `groups[max_freq]`, decrement that value's count, and if the layer becomes empty, decrement `max_freq`.

Because a value on layer `f` was also pushed onto layers `1..f-1`, removing it from the top layer leaves it correctly represented at its lower frequency.

## Code

```python
class FreqStack:
    def __init__(self):
        self.cnt = {}
        self.maxCnt = 0
        self.stacks = {}

    def push(self, val: int) -> None:
        valCnt = 1 + self.cnt.get(val, 0)
        self.cnt[val] = valCnt
        if valCnt > self.maxCnt:
            self.maxCnt = valCnt
            self.stacks[valCnt] = []
        self.stacks[valCnt].append(val)

    def pop(self) -> int:
        res = self.stacks[self.maxCnt].pop()
        self.cnt[res] -= 1
        if not self.stacks[self.maxCnt]:
            self.maxCnt -= 1
        return res
```

## Complexity

- **Time:** `O(1)` per operation — each push and pop does a constant number of hash map and list operations.
- **Space:** `O(n)` — each pushed element is stored once in `groups`, plus one count per distinct value.

## Other Approaches

- **Max-heap with timestamps:** store `(frequency, insertion index, value)` in a heap and pop the largest — Time `O(log n)` per operation / Space `O(n)`

## C++

```cpp
class FreqStack {
    unordered_map<int, int> cnt;
    vector<vector<int>> stacks;

public:
    void push(int val) {
        int k = ++cnt[val];
        if (k > stacks.size())
            stacks.push_back({val});
        else
            stacks[k - 1].push_back(val);
    }

    int pop() {
        int val = stacks.back().back();
        stacks.back().pop_back();
        if (stacks.back().empty())
            stacks.pop_back();
        --cnt[val];
        return val;
    }
};
```
