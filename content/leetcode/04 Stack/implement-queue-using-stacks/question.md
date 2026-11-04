---
video: https://www.youtube.com/watch?v=eanwa3ht3YQ
topic: "Stack"
difficulty: Easy
leetcode: https://leetcode.com/problems/implement-queue-using-stacks/
neetcode: https://neetcode.io/problems/implement-queue-using-stacks
---
# Implement Queue using Stacks

**Topic:** Stack · **Difficulty:** Easy

## Problem

Build a first-in-first-out (FIFO) queue using only two stacks. The queue must support the usual operations: push, peek, pop, and empty.

Implement the `MyQueue` class:

- `void push(int x)` pushes element `x` to the back of the queue.
- `int pop()` removes the element from the front of the queue and returns it.
- `int peek()` returns the element at the front of the queue.
- `boolean empty()` returns `true` if the queue is empty, `false` otherwise.

Notes:

- Only standard stack operations are allowed: push to top, peek/pop from top, size, and is-empty.
- If your language has no built-in stack, you may simulate one with a list or deque, as long as you use only a stack's standard operations.

Follow-up: can you make each operation amortized O(1)? That is, n operations should take O(n) time overall, even if a single operation occasionally takes longer.

## Examples

**Example 1**
```text
Input
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 1, 1, false]
```

Explanation:

```text
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek();  // return 1
myQueue.pop();   // return 1, queue is [2]
myQueue.empty(); // return false
```

## Constraints

- `1 <= x <= 9`
- At most `100` calls will be made to `push`, `pop`, `peek`, and `empty`.
- All the calls to `pop` and `peek` are valid.
