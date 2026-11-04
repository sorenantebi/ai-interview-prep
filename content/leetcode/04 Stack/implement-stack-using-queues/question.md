---
video: https://www.youtube.com/watch?v=rW4vm0-DLYc
topic: "Stack"
difficulty: Easy
leetcode: https://leetcode.com/problems/implement-stack-using-queues/
neetcode: https://neetcode.io/problems/implement-stack-using-queues
---
# Implement Stack using Queues

**Topic:** Stack · **Difficulty:** Easy

## Problem

Build a last-in-first-out (LIFO) stack using only queues. The stack must support `push`, `top`, `pop`, and `empty` like a normal stack.

Implement the `MyStack` class:

- `void push(int x)` pushes element `x` onto the top of the stack.
- `int pop()` removes the element on top of the stack and returns it.
- `int top()` returns the element on top of the stack without removing it.
- `boolean empty()` returns `true` if the stack is empty, `false` otherwise.

You may only use the standard queue operations: push to back, peek/pop from front, size, and is-empty. If your language has no built-in queue, you can simulate one with a list or deque, as long as you only use those operations.

**Follow-up:** Can you implement the stack using only one queue?

## Examples

**Example 1**
```text
Input
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 2, 2, false]
```

Explanation:
```text
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top();   // returns 2
myStack.pop();   // returns 2
myStack.empty(); // returns false
```

## Constraints

- `1 <= x <= 9`
- At most `100` calls will be made to `push`, `pop`, `top`, and `empty`.
- All calls to `pop` and `top` are valid.
