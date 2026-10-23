---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/min-stack/
neetcode: https://neetcode.io/problems/minimum-stack
---
# Min Stack

**Topic:** Stack · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/min-stack/) · [NeetCode](https://neetcode.io/problems/minimum-stack)

## Problem

Design a stack that, in addition to the usual operations, can report its smallest element in constant time. Implement the class `MinStack`:

- `MinStack()` — initializes an empty stack.
- `push(val)` — pushes `val` onto the stack.
- `pop()` — removes the top element.
- `top()` — returns the top element.
- `getMin()` — returns the minimum element currently in the stack.

Every method must run in `O(1)` time. `pop`, `top` and `getMin` are only called when the stack is non-empty.

## Examples

**Example 1**
```text
Input:  ["MinStack","push","push","push","getMin","pop","top","getMin"]
        [[],[-2],[0],[-3],[],[],[],[]]
Output: [null,null,null,null,-3,null,0,-2]
```

**Example 2**
```text
Input:  ["MinStack","push","push","getMin","pop","getMin"]
        [[],[1],[1],[],[],[]]
Output: [null,null,null,1,null,1]
Explanation: duplicate minimums must survive a pop
```

## Constraints

- `-2^31 <= val <= 2^31 - 1`
- `pop`, `top`, `getMin` are always called on a non-empty stack
- At most `3 * 10^4` calls in total
