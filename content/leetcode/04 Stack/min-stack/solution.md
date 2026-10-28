---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/min-stack/
neetcode: https://neetcode.io/problems/minimum-stack
---
# Min Stack - Solution

**Question:** Min Stack - Question · **Difficulty:** Medium

## Intuition

The minimum of a stack only changes when elements are pushed or popped at the top, so the minimum "as of" each element is fixed once it is pushed. Storing that running minimum alongside each element means `getMin` is just a lookup on the top entry.

## Approach

1. Keep one stack of `(value, min_so_far)` pairs.
2. `push(val)`: the new minimum is `min(val, current_min)` (or `val` if empty); push the pair.
3. `pop()`: pop the pair — the previous pair automatically holds the previous minimum.
4. `top()` / `getMin()`: read the first / second field of the top pair.

## Code

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.minStack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        val = min(val, self.minStack[-1] if self.minStack else val)
        self.minStack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]
```

## Complexity

- **Time:** `O(1)` for every operation.
- **Space:** `O(n)` — one extra value stored per element.

## Other Approaches

- **Separate min stack:** push onto a second stack only when `val <= current min`, and pop it when the popped value equals its top — Time `O(1)`, Space `O(n)` worst case but often less.
- **Difference encoding:** store `val - min` and recover the old minimum on pop from negative differences — Time `O(1)`, Space `O(1)` extra (but tricky with overflow in fixed-width languages).

## Key Takeaway

To answer an aggregate query (min/max) on a stack in O(1), store the aggregate snapshot with each element — the stack's LIFO nature means snapshots never go stale.

## C++

```cpp
/*
    Design stack that supports push, pop, top, & retriving min element
    
    2 stacks, 1 normal & 1 monotonic decr, only push if lower than top
    
    Time: O(1)
    Space: O(n)
*/

class MinStack {
public:
    MinStack() {
        
    }
    
    void push(int val) {
        stk.push(val);
        
        if (minStk.empty() || val < minStk.top().first) {
            minStk.push({val, 1});
        } else if (val == minStk.top().first) {
            minStk.top().second++;
        }
    }
    
    void pop() {
        if (stk.top() == minStk.top().first) {
            minStk.top().second--;
            if (minStk.top().second == 0) {
                minStk.pop();
            }
        }
        stk.pop();
    }
    
    int top() {
        return stk.top();
    }
    
    int getMin() {
        return minStk.top().first;
    }
private:
    stack<int> stk;
    stack<pair<int, int>> minStk;
};

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack* obj = new MinStack();
 * obj->push(val);
 * obj->pop();
 * int param_3 = obj->top();
 * int param_4 = obj->getMin();
 */
```
