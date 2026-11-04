---
video: https://www.youtube.com/watch?v=Z6idIicFDOE
topic: "Stack"
difficulty: Hard
leetcode: https://leetcode.com/problems/maximum-frequency-stack/
neetcode: https://neetcode.io/problems/maximum-frequency-stack
---
# Maximum Frequency Stack

**Topic:** Stack · **Difficulty:** Hard

## Problem

Design a stack-like data structure that supports pushing integers and popping the most frequent one.

Implement the `FreqStack` class:

- `FreqStack()` creates an empty frequency stack.
- `void push(int val)` pushes the integer `val` onto the top of the stack.
- `int pop()` removes and returns the most frequent element in the stack. If several elements are tied for most frequent, the one closest to the top of the stack is removed and returned.

## Examples

**Example 1**
```text
Input:
["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]
[[], [5], [7], [5], [7], [4], [5], [], [], [], []]
Output:
[null, null, null, null, null, null, null, 5, 7, 5, 4]
```

Explanation: after the six pushes the stack is `[5,7,5,7,4,5]`.
- `pop()` returns `5` (most frequent); the stack becomes `[5,7,5,7,4]`.
- `pop()` returns `7` (5 and 7 tie, 7 is closer to the top); the stack becomes `[5,7,5,4]`.
- `pop()` returns `5` (most frequent); the stack becomes `[5,7,4]`.
- `pop()` returns `4` (5, 7 and 4 all tie, 4 is closest to the top); the stack becomes `[5,7]`.

## Constraints

- `0 <= val <= 10^9`
- At most `2 * 10^4` calls will be made to `push` and `pop`.
- It is guaranteed that there will be at least one element in the stack before calling `pop`.
